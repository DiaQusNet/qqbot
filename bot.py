# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message

from features.ollama_replay import messages_with_id, clean_memory, reply

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        if '/记忆清除' in message.content:
            clean_memory()
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content='记忆被清除了...')
            _log.info(messageResult)

        else:
            message_list = messages_with_id(message.author.member_openid, message.group_openid, message.content)
            ai_message = reply(message_list)
            messages_with_id(message.author.member_openid, message.group_openid, ai_message, True)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=ai_message)
            _log.info(messageResult)


if __name__ == "__main__":

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
