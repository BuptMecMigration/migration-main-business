import time
import random

class Token(object):
    # user ID generation
    @classmethod
    def gen_user_token(cls):
        token = time.time().__int__()+random.randint(0,9999)
        return token
    @classmethod
    # 目前暂时使用user_token的函数吧
    def gen_service_token(cls):
        return cls.gen_user_token()