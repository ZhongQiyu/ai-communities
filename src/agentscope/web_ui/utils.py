# -*- coding: utf-8 -*-
import os
import pickle
import time
from http import HTTPStatus
from typing import List
from datetime import datetime

import gradio as gr
import base64
import dashscope

import requests
from colorist import BgBrightColor
import inquirer
import random
from multiprocessing import Queue, Value
from collections import defaultdict
from dataclasses import dataclass

from pathlib import Path

from dashscope import Generation
from pypinyin import lazy_pinyin, Style

import hashlib
from PIL import Image

SYS_MSG_PREFIX = "【系统】"
DEFAULT_AGENT_IMG_DIR = "/tmp/as_game/config/"
OPENING_ROUND = 3
REVISION_ROUND = 3

USE_WEB_UI = False

MAX_ROLE_NUM = 20


def speak_print(m):
    print(f"{BgBrightColor.BLUE}{m.name}{BgBrightColor.OFF}: {m.content}")


def get_use_web_ui():
    global USE_WEB_UI
    return USE_WEB_UI


def disable_web_ui():
    global USE_WEB_UI
    USE_WEB_UI = False


def enable_web_ui():
    global USE_WEB_UI
    USE_WEB_UI = True


def init_uid_queues():
    return {
        "glb_queue_chat_msg": Queue(),
        "glb_queue_chat_input": Queue(),
        "glb_queue_reset_msg": Queue(),
    }


glb_uid_dict = defaultdict(init_uid_queues)


def send_chat_msg(
    msg,
    role=None,
    uid=None,
    flushing=False,
    avatar="./assets/bot.jpg",
    id=None,
):
    # print("send_chat_msg uid: ", uid)
    print("send_chat_msg:", msg)
    if get_use_web_ui():
        global glb_uid_dict
        glb_queue_chat_msg = glb_uid_dict[uid]["glb_queue_chat_msg"]
        glb_queue_chat_msg.put(
            [
                None,
                {
                    "text": msg,
                    "name": role,
                    "flushing": flushing,
                    "avatar": avatar,
                    "id": id,
                },
            ],
        )


def send_player_msg(
    msg,
    role="我",
    uid=None,
    flushing=False,
    avatar="./assets/user.jpg",
):
    print("send_player_msg:", msg)
    if get_use_web_ui():
        global glb_uid_dict
        glb_queue_chat_msg = glb_uid_dict[uid]["glb_queue_chat_msg"]
        glb_queue_chat_msg.put(
            [
                {
                    "text": msg,
                    "name": role,
                    "flushing": flushing,
                    "avatar": avatar,
                },
                None,
            ],
        )


def get_chat_msg(uid=None):
    global glb_uid_dict
    glb_queue_chat_msg = glb_uid_dict[uid]["glb_queue_chat_msg"]
    if not glb_queue_chat_msg.empty():
        line = glb_queue_chat_msg.get(block=False)
        # print("get_chat_msg line: ", line)
        if line is not None:
            return line
    return None


def send_player_input(msg, role="餐厅老板", uid=None):
    if get_use_web_ui():
        global glb_uid_dict
        glb_queue_chat_input = glb_uid_dict[uid]["glb_queue_chat_input"]
        glb_queue_chat_input.put([None, msg])


def send_pretty_msg(msg, uid=None, flushing=True, avatar="./assets/bot.jpg"):
    speak_print(msg)
    if get_use_web_ui():
        global glb_uid_dict
        send_chat_msg(
            msg.content,
            uid=uid,
            role=msg.name,
            flushing=flushing,
            avatar=avatar,
        )


def get_player_input(name=None, uid=None):
    global glb_uid_dict
    if get_use_web_ui():
        print("wait queue input")
        glb_queue_chat_input = glb_uid_dict[uid]["glb_queue_chat_input"]
        content = glb_queue_chat_input.get(block=True)[1]
        print(content)
        if content == "**Reset**":
            glb_uid_dict[uid] = init_uid_queues()
            raise ResetException
    else:
        content = input(f"{name}: ")
    return content

def send_reset_msg(msg, uid=None):
    if get_use_web_ui():
        global glb_uid_dict
        glb_queue_reset_msg = glb_uid_dict[uid]["glb_queue_reset_msg"]
        if glb_queue_reset_msg.empty():
            glb_queue_reset_msg.put([None, msg])

def get_reset_msg(name=None, uid=None):
    global glb_uid_dict
    if get_use_web_ui():
        print("wait queue input")
        glb_queue_reset_msg = glb_uid_dict[uid]["glb_queue_reset_msg"]
        if not glb_queue_reset_msg.empty():
            content = glb_queue_reset_msg.get(block=True)[1]
            print(content)
            if content == "**Reset**":
                glb_uid_dict[uid] = init_uid_queues()
                time.sleep(1)
                raise ResetException
    return None


def query_answer(questions: List, key="ans", uid=None):
    if get_use_web_ui():
        return get_player_input(uid=uid)
    else:
        answer = [inquirer.prompt(questions)[key]]  # return list
    return answer


class ResetException(Exception):
    pass



def cycle_dots(text: str, num_dots: int = 3) -> str:
    # 计算当前句尾的点的个数
    current_dots = len(text) - len(text.rstrip("."))
    # 计算下一个状态的点的个数
    next_dots = (current_dots + 1) % (num_dots + 1)
    if next_dots == 0:
        # 避免 '...0', 应该是 '.'
        next_dots = 1
    # 移除当前句尾的点，并添加下一个状态的点
    return text.rstrip(".") + "." * next_dots


def check_uuid(uid):
    if not uid or uid == "":
        if os.getenv("MODELSCOPE_ENVIRONMENT") == "studio":
            raise gr.Error("请登陆后使用! (Please login first)")
        else:
            uid = "local_user"
    return uid


def extract_keys_from_dict(input_dict, keys_list):
    return {k: input_dict[k] for k in keys_list if k in input_dict}


def get_next_element(lst, element):
    if element not in lst:
        # Return the first if not in list
        return lst[0]

    next_index = lst.index(element) + 1
    if next_index >= len(lst):
        next_index = 0

    return lst[next_index]


def generate_image_from_name(name):
    from agentscope.file_manager import file_manager
    current_path = file_manager.dir_root
    print(f"current_path of {name}", current_path)
    # Using hashlib to generate a hash of the name
    hash_func = hashlib.md5()
    hash_func.update(name.encode('utf-8'))
    hash_value = hash_func.hexdigest()

    # Extract the first 6 characters of the hash value as the hexadecimal
    # representation of the color
    # generate a color value between #000000 and #ffffff
    color_hex = '#' + hash_value[:6]
    color_rgb = Image.new('RGB', (1, 1), color_hex).getpixel((0, 0))

    image_filepath = os.path.join(current_path, f"{name}_image.png")

    if os.path.exists(image_filepath):
        print(f"Image already exists at {image_filepath}")
        return image_filepath

    # generate image
    width, height = 200, 200
    image = Image.new('RGB', (width, height), color_rgb)

    # save image
    image.save(image_filepath)
    # print(f"Image saved as {image_filepath}")

    return image_filepath
