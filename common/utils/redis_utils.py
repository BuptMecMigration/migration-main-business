# -*- coding: utf-8 -*-
import redis

from common.redis_config import REDIS_DB_URL
from common.utils.serialize_utils import Serializer


def connect_redis():
    return redis.Redis(host=REDIS_DB_URL.HOST.value, port=REDIS_DB_URL.PORT.value,
                       password=REDIS_DB_URL.PASSWORD.value, db=REDIS_DB_URL.DB.value,
                       )
    # decode_responses = True 该选项设置为true会使得存储方式采用字符串进行，如果采取pickle则该参数应该采取默认值


class RedisUtil(object):

    redis_conn: redis.Redis = connect_redis()

    @classmethod
    def get_redis_data(cls, key: str):
        data = cls.redis_conn.get(key)
        if data is None:
            return None
        return Serializer.pickle_deserialize(data)

    @classmethod
    def set_redis_data(cls, key, value):
        data = Serializer.pickle_serialize(value)
        cls.redis_conn.set(
            name=key,
            value=data,
            # 默认redis过期时间，不设置代表不过期
            # ex=Config.EXPIRES_TIME
        )

