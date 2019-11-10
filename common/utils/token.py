import time
import random

class Token(object):
    # user ID generation
    @classmethod
    def gen_token(cls):
        token = time.time().__int__()+random.randint(0,9999)
        return token
