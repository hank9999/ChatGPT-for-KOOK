import json
import logging
import sys

kook_token = ''
openai = {}


def load():
    global kook_token, openai
    with open('config.json', 'r', encoding='utf-8') as f:
        conf = json.loads(f.read())
        # if ('kook' not in conf and 'token' not in conf['kook']) \ or ('openai' not in conf and ('email' not in
        # conf['openai'] or 'password' not in conf['openai'] or 'proxy' not in conf['openai'])):
        if ('kook' not in conf and 'token' not in conf['kook']) or ('openai' not in conf):
            logging.error("配置文件错误")
            sys.exit()
        if len(conf['kook']['token']) == 0:
            logging.error("缺少 KOOK 的 Token")
            sys.exit()
        if len(conf['openai']['session_token']) == 0 or len(conf['openai']['cf_clearance']) == 0:
            logging.error("OpenAI session_token 或 cf_clearance 为空")
            sys.exit()

        kook_token = conf['kook']['token']
        openai = conf['openai']
