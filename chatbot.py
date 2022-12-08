import datetime

import config
import logging
from asyncChatGPT.asyncChatGPT import Chatbot


class ChatSession:
    def __init__(self, conversation_id=None):
        self.chatbot = None


bots = {}


# Refer to https://github.com/lss233/chatgpt-mirai-qq-bot
# Refer to https://github.com/acheong08/ChatGPT
def find_or_create_chatbot(bot_id: str):
    if bot_id in bots:
        return bots[bot_id]
    else:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", f"Generating new chatbot session for id {bot_id}")
        bot = Chatbot({'email': config.openai_email, 'password': config.openai_password, 'proxy': config.openai_proxy}, conversation_id=None)
        bot.reset_chat()
        bot.refresh_session()
        bots[bot_id] = bot
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", f"Generating ok for id {bot_id}")
        return bot
