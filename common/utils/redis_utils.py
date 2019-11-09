# -*- coding: utf-8 -*-
import redis

from common.redis_config import REDIS_DB_URL


def connect_redis():
    return redis.Redis(REDIS_DB_URL)


class RedisUtil(object):

    redis_conn: redis.Redis

    @classmethod
    def get_redis_data(cls, key: str):
        conn = connect_redis()
        data = conn.get(key)
        return data

    @classmethod
    def set_redis_data(cls, key, value):
        conn = connect_redis()
        data = value
        conn.set(
            name=key,
            value=data,
            # 默认redis国企时间，不设置代表不过期
            # ex=Config.EXPIRES_TIME
        )

    def __init__(self) -> None:
        self.redis_conn = connect_redis()
