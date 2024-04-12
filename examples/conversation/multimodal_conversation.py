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
from agentscope.agents.edit_image_agent import EditImageAgent
from agentscope.agents.user_agent import UserAgent
from agentscope.web_ui.utils import send_chat_msg, query_answer, \
    generate_image_from_name, ResetException
from OSSUtil import getBucketByPackagerepository, upload_file_2_oss, downloadOSSFile
import pika

config = {
'MQ_PORT' : 5672,
'VIRTUAL_HOST' : '/',
'OSS_UPLOAD_IMAGE_DIR' : 'deco_upload',
}


def main():
    bucket_str = 'livedeco-test'
    bucket = getBucketByPackagerepository(bucket_str)

    credentials = pika.PlainCredentials(os.getenv('MQ_USER_NAME'), os.getenv('MQ_PASSWORD'))
    node = pika.ConnectionParameters(host=os.getenv('MQ_HOST'), port=config['MQ_PORT'],
                                     virtual_host=config['VIRTUAL_HOST'],
                                     credentials=credentials, connection_attempts=5, retry_delay=5)
    connection = pika.BlockingConnection([node])
    channel = connection.channel()


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
        bucket=bucket,
        connection=connection,
        channel=channel,
        sys_prompt="你是一个图片生成助手",
    )

    edit_image_agent = EditImageAgent(
        name="效果图编辑成助手",
        bucket=bucket,
        connection=connection,
        channel=channel,
        model_config_name="gpt-3.5-turbo",
        sys_prompt="""请按照以下格式输出JSON数据，不要添加任何额外的文字或解释。对于用户的室内设计编辑需求，将其转换成指定的JSON结构，并转成英文，注意json中只能有英文。

格式：
{
  "source_furniture": "原始家具名称",
  "desired_furniture": "用户想要的家具名称"
}

例子：
用户输入：“请把墙上的画改成一张有可爱小姑娘的图片”；
输出应为：{"source_furniture":"picture on the wall", "desired_furniture":"picture with a lovely girl"}

用户输入：“地毯改成花纹地毯”；
输出应为：{"source_furniture":"carpet", "desired_furniture":"patterned carpet"}

现在，请根据用户的输入，转换并输出为严格的JSON格式，并转成英文，注意json中只能有英文。
        """
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
        edit_image_avatar = generate_image_from_name(edit_image_agent.name)

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
                time.sleep(0.1)
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
                time.sleep(0.1)
                send_chat_msg(
                    f"请在列表中选择。",
                    uid=uid,
                    avatar=master_avatar,
                )
                continue
            break


        send_chat_msg(f"请在右边“图片输入”框内上传一张待装修的房间照片，并点击下方的“生成效果图”。不上传图片也可以点击“生成效果图”，系统将随机生成对于效果图。",
                          role=master_agent.name,
                          flushing=True,
                          uid=uid,
                          avatar=master_avatar)
        while True:
            try:
                msg = user_agent()
                source_image = msg["content"]
                # print("图片信息：", msg)
                time.sleep(0.1)
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
                created_image_oss_key = decoration_generate_agent({"room_type": answer_room_type, "room_style": answer_room_style, "source_image": source_image})
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

        send_chat_msg(f"您可以在右下方输入文字对生成的效果图进行编辑。比如“请把墙上的画改成一张有可爱小姑娘的图片”、“地毯改成花纹地毯”",
                      role=master_agent.name,
                      flushing=True,
                      uid=uid,
                      avatar=master_avatar)
        while True:
            try:
                msg = user_agent()
                user_input = msg["content"]
                # print("图片信息：", msg)
                time.sleep(0.1)
                send_chat_msg(f"已收到信息，正在编辑效果图，请稍等",
                              role=edit_image_agent.name,
                              flushing=True,
                              uid=uid,
                              avatar=edit_image_avatar)
                edit_image_agent({"image_path": created_image_oss_key, "user_input": user_input})
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
