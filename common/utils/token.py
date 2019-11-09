import time
import random


class Token(object):
    prefix = str(random.randint(0,9999999999))
    conter = 0

    # user ID generation
    @classmethod
    def gen_token(cls, key: str):
        token = cls.prefix + str(cls.conter)
        cls.conter += 1
        return token
