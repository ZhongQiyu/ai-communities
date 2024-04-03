# -*- coding: utf-8 -*-
"""A simple example for audio conversation between user and assistant agent."""
import json
import os
import threading
import time

import inquirer

import agentscope
from agentscope.agents.dialog_agent import DialogAgent
from agentscope.agents.decoration_generate_agent import DecorationGenerateAgent
from agentscope.agents.user_agent import UserAgent
from agentscope.web_ui.utils import send_chat_msg, query_answer, \
    generate_image_from_name, ResetException


def main():
    agentscope.init(
        model_configs=[
            {
                "config_name": "gpt-3.5-turbo",  # 用于识别配置的名称
                "model_type": "dashscope_chat",
                "model_name": "qwen-max-1201",  # dashscope 中的模型
                "api_key": os.getenv('OPENAI_API_KEY'),
            },
            {
                "model_type": "post_api_dalle",
                "config_name": "dall_e",
                "api_url": "xxx",
                "headers": {
                    "Content-Type": "xxx",
                    "Authorization": "Bearer xxx",
                },
                "json_args": {
                    "model": "dall-e-3",
                    "n": 1,
                    "size": "1024x1024",
                },
                "messages_key": "prompt",
            }
        ]
    )
    # Init agents
    master_agent = DialogAgent(
        name="指挥官",
        sys_prompt="你是一个人工智能助手。",
        model_config_name="gpt-3.5-turbo",  # replace by your model config name
    )

    decoration_generate_agent = DecorationGenerateAgent(
        name="室内设计效果图生成助手",
        bucket_str='livedeco-test',
        sys_prompt="你是一个图片生成助手",
    )

    user_agent = UserAgent()

    thread_name = threading.current_thread().name
    uid = thread_name
    # start the conversation between user and assistant

    x = None
    while x is None or x.content != "退出。":
        master_avatar = generate_image_from_name(master_agent.name)
        # sadtalker_avatar = generate_image_from_name(sadtalker_agent.name)
        decoration_generate_avatar = generate_image_from_name(decoration_generate_agent.name)

        send_chat_msg(
            f"您好，欢迎体验未来空间多模态应用，您可以上传一张待装修的房间照片、选择房间类型和装修风格，就会生成对应装修效果图。",
            role=master_agent.name,
            flushing=True,
            uid=uid,
            avatar=master_avatar)

        choose_room_type = f"""首先，请选择需要装修的房间类型
                            <select-box shape="card" item-width="auto" type="checkbox" options=
                            '{json.dumps(["客餐厅", "客厅", "餐厅", "卧室", "卫生间", "书房"])}'
                                                 select-once></select-box>"""
        send_chat_msg(choose_room_type,
                      role=master_agent.name,
                      flushing=False,
                      uid=uid,
                      avatar=master_avatar)

        questions_room_type = [
            inquirer.List(
                "ans",
                message=f"请选择一种房间类型",
                choices=["客餐厅", "客厅", "餐厅", "卧室", "卫生间", "书房"],
            ),
        ]
        while True:
            answer_room_type = query_answer(questions_room_type, "ans", uid=uid)
            if isinstance(answer_room_type, str):
                time.sleep(0.5)
                send_chat_msg(
                    f"请在列表中选择。",
                    uid=uid,
                    avatar=master_avatar,
                )
                continue
            break

        choose_room_style = f"""请选择需要装修的风格
                                    <select-box shape="card" item-width="auto" type="checkbox" options=
                                    '{json.dumps(["现代风", "轻奢风", "奶油风", "侘寂风", "新中式", "黑白灰"])}'
                                                         select-once></select-box>"""
        send_chat_msg(choose_room_style,
                      role=master_agent.name,
                      flushing=False,
                      uid=uid,
                      avatar=master_avatar)

        questions_room_style = [
            inquirer.List(
                "ans",
                message=f"请选择一种装修风格",
                choices=["现代风", "轻奢风", "奶油风", "侘寂风", "新中式", "黑白灰"],
            ),
        ]
        while True:
            answer_room_style = query_answer(questions_room_style, "ans", uid=uid)
            if isinstance(answer_room_style, str):
                time.sleep(0.5)
                send_chat_msg(
                    f"请在列表中选择。",
                    uid=uid,
                    avatar=master_avatar,
                )
                continue
            break


        send_chat_msg(f"请在下方“图片输入”框内上传一张待装修的房间照片，并点击最下方的“发送图片”按钮进行发送",
                          role=master_agent.name,
                          flushing=True,
                          uid=uid,
                          avatar=master_avatar)
        while True:
            try:
                msg = user_agent()
                source_image = msg["content"]
                # print("图片信息：", msg)
                time.sleep(0.5)
                send_chat_msg(f"接下来，图片生成助手会生成对应的效果图",
                              role=master_agent.name,
                              flushing=True,
                              uid=uid,
                              avatar=master_avatar)
                send_chat_msg(f"已收到信息，正在校验并将其转化为对应的效果图，请稍等",
                              role=decoration_generate_agent.name,
                              flushing=True,
                              uid=uid,
                              avatar=decoration_generate_avatar)
                decoration_generate_agent({"room_type": answer_room_type, "room_style": answer_room_style, "source_image": source_image})
                break
            except ResetException as e:
                raise e
            except Exception as e:
                    print("exception: ", e)
                    send_chat_msg(f"对不起，您没有上传图片或者您上传的图片不符合要求，请重新上传一张图片",
                                  role=master_agent.name,
                                  flushing=True,
                                  uid=uid,
                                  avatar=master_avatar)



if __name__ == "__main__":
    main()
