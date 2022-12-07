import datetime
from typing import List

from khl import Bot, Message
from khl.command import Lexer, Exceptions

import chatbot
import config

bot: Bot


class KeyWord(Lexer):
    keyword: str
    start_with: bool
    no_space: bool

    def __init__(self, keyword: str, start_with: bool = True, no_space: bool = False):
        self.keyword = keyword
        self.start_with = start_with
        self.no_space = no_space

    def lex(self, msg: Message) -> List[str]:
        if self.no_space:
            command = msg.content.split('\n')[0].strip()
            if command != self.keyword:
                raise Exceptions.Lexer.NotMatched(msg)
        elif self.start_with:
            command = msg.content.split(' ')[0].strip()
            if command != self.keyword:
                raise Exceptions.Lexer.NotMatched(msg)
        else:
            if msg.content.find(self.keyword) < 0:
                raise Exceptions.Lexer.NotMatched(msg)
        return []


def init():
    global bot
    bot = Bot(token=config.kook_token)

    @bot.command(lexer=KeyWord(keyword='/chat', start_with=True))
    async def chat(msg: Message):
        content = msg.content.removeprefix('/chat').strip()
        if len(content) == 0:
            await msg.reply(
                '您好！我是 ChatGPT，一个由 OpenAI 训练的大型语言模型。我不是真正的人，而是一个计算机程序，可以通过文本聊天来帮助您解决问题。'
                '如果您有任何问题，请随时告诉我，我将尽力回答。\n如需重置会话，请回复`/reset`。\n')
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]",
              f'用户: {msg.author.nickname}#{msg.author_id}, 服务器: {msg.ctx.guild.name}#{msg.ctx.guild.id}, '
              f'问题: {content}, 等待 API 响应...')
        cbot = chatbot.find_or_create_chatbot(msg.author_id)
        try:
            resp = cbot.get_chat_response(content, output="text")
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]",
                  f'用户: {msg.author.nickname}#{msg.author_id}, 服务器: {msg.ctx.guild.name}#{msg.ctx.guild.id}, '
                  f'问题: {content}, 回答: {resp}')
            await msg.reply(resp["message"])
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]",
                  f'用户: {msg.author.nickname}#{msg.author_id}, 服务器: {msg.ctx.guild.name}#{msg.ctx.guild.id}, '
                  f'出现故障！会话已重置。{e}')
            cbot.reset_chat()
            cbot.refresh_session()
            await msg.reply('出现故障！会话已重置。\n' + str(e))

    @bot.command(lexer=KeyWord(keyword='/reset', start_with=True))
    async def reset(msg: Message):
        cbot = chatbot.find_or_create_chatbot(msg.author_id)
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]",
              f"用户: {msg.author.nickname}#{msg.author_id}, 服务器: {msg.ctx.guild.name}#{msg.ctx.guild.id}, 重置会话")
        cbot.reset_chat()
        cbot.refresh_session()
        await msg.reply('会话已重置。')
