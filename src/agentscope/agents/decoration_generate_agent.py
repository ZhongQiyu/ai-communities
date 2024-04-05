# -*- coding: utf-8 -*-
"""Class for Sadtalker Agent"""
import threading
from typing import Optional
import pika
import uuid
from loguru import logger

from agentscope.message import Msg
from agentscope.agents.agent import AgentBase
from agentscope.web_ui.utils import generate_image_from_name, send_chat_msg
import requests
import os
import json
from OSSUtil import getBucketByPackagerepository, upload_file_2_oss, downloadOSSFile

config = {
'MQ_HOST' : 'mq-test.123kanfang.com',
'MQ_USER_NAME' : 'livedecoservice',
'MQ_PASSWORD' : 'a498cd8e2372409eaca8f1eee5000b51',
'QUEUE_NAME' : 'CN.AIGC.Add.Command',
'MQ_PORT' : 5672,
'VIRTUAL_HOST' : '/',
'OSS_UPLOAD_IMAGE_DIR' : 'deco_upload',
}


class DecorationGenerateAgent(AgentBase):
    """Class for VideoAgent"""

    def __init__(
            self,
            name: str,
            bucket_str: str,
            sys_prompt: Optional[str] = None,
            model_config_name: str = None,
            use_memory: bool = True,
            memory_config: Optional[dict] = None,
    ) -> None:
        """Initialize the text to image agent.

        Arguments:
            name (`str`):
                The name of the agent.
            sys_prompt (`Optional[str]`):
                The system prompt of the agent, which can be passed by args
                or hard-coded in the agent.
            model_config_name (`str`, defaults to None):
                The name of the model config, which is used to load model from
                configuration.
            use_memory (`bool`, defaults to `True`):
                Whether the agent has memory.
            memory_config (`Optional[dict]`):
                The config of memory.
        """
        super().__init__(
            name=name,
            sys_prompt=sys_prompt,
            # model_config_name=model_config_name,
            use_memory=use_memory,
            memory_config=memory_config,
        )
        self.bucket_str = bucket_str
        self.bucket = getBucketByPackagerepository(self.bucket_str)

        credentials = pika.PlainCredentials(config['MQ_USER_NAME'], config['MQ_PASSWORD'])
        node = pika.ConnectionParameters(host=config['MQ_HOST'], port=config['MQ_PORT'],
                                         virtual_host=config['VIRTUAL_HOST'],
                                         credentials=credentials, connection_attempts=5, retry_delay=5)

        self.connection = pika.BlockingConnection([node])

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        self.image_dir = 'local_images'

    def reply(self, x: dict = None) -> dict:
        """Forward method for agent"""
        self.memory.add(x)
        source_image = x["source_image"]
        room_type = x["room_type"][0]
        room_style = x["room_style"][0]
        self.corr_id = str(uuid.uuid4())

        image_oss_key = os.path.join(config['OSS_UPLOAD_IMAGE_DIR'], self.corr_id + '.jpg')
        if source_image:
            self.upload_image(image_oss_key, source_image)

        room_type_map = {
            "客餐厅": "living_dining_room",
            "客厅": "living_room",
            "餐厅": "dining_room",
            "卧室": "bedroom",
            "卫生间": "bathroom",
            "书房": "study_room"
        }
        room_style_map = {
            "现代风": "modern",
            "轻奢风": "qingshe",
            "奶油风": "naiyoufeng",
            "侘寂风": "chaji",
            "新中式": "chinese",
            "黑白灰": "heibaihui"
        }
        message = {
            "bucket": "livedeco-test",
            "sourceUrl": image_oss_key,
            "packageId": self.corr_id,
            "style": room_style_map[room_style],
            "roomType": room_type_map[room_type]
        }
        if source_image is None:
            message["request_type"] = 'wst'
            message["sourceUrl"] = ''
        message = json.dumps(message)


        self.response = None
        self.channel.basic_publish(exchange=config['QUEUE_NAME'],
                                   routing_key=config['QUEUE_NAME'],
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(message))
        while self.response is None:
            self.connection.process_data_events()
        current_img_dir = os.path.join(self.image_dir, self.corr_id)
        if not os.path.exists(current_img_dir):
            os.makedirs(current_img_dir)
        created_image_oss_key = 'AIGCs/' + self.corr_id + '/0.png'
        downloadOSSFile(self.bucket, created_image_oss_key, current_img_dir)

        msg = Msg(self.name, os.path.join(current_img_dir, '0.png'))
        self.memory.add(msg)
        self.speak(msg)
        return msg


    def speak(self, x):
        logger.chat(x)
        thread_name = threading.currentThread().name
        if thread_name != "MainThread":
            avatar = generate_image_from_name(self.name)
            # msg = f"""这是生成的视频
            # <video src="{x["content"]}"></video>"""
            msg = f"""这是生成的装修效果图
                                <img src="{x["content"]}" />
                                """
            send_chat_msg(msg, role=self.name,
                          uid=thread_name, avatar=avatar)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def upload_image(self, image_oss_key, local_image_path):
        # 获得文件后缀名
        try:
            upload_file_2_oss(self.bucket, image_oss_key, local_image_path)
        except Exception as e:
            logger.error(f"上传图片失败，错误信息：{e}")
            return False