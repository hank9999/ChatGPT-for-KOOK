import json
import logging
import sys

kook_token = ''
openai_email = ''
openai_password = ''
openai_proxy = ''

def load():
    global kook_token, openai_email, openai_password, openai_proxy
    with open('config.json', 'r', encoding='utf-8') as f:
        conf = json.loads(f.read())
        if ('kook' not in conf and 'token' not in conf['kook']) \
                or ('openai' not in conf and ('email' not in conf['openai'] or 'password' not in conf['openai'] or 'proxy' not in conf['openai'])):
            logging.error("配置文件错误")
            sys.exit()
        if len(conf['kook']['token']) == 0:
            logging.error("缺少 KOOK 的 Token")
            sys.exit()
        if len(conf['openai']['email']) == 0 or len(conf['openai']['password']) == 0:
            logging.error("OpenAI 用户名或密码为空")
            sys.exit()

        kook_token = conf['kook']['token']
        openai_email = conf['openai']['email']
        openai_password = conf['openai']['password']
        openai_proxy = conf['openai']['proxy']
