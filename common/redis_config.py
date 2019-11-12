# -*- coding: utf-8 -*-
# redis配置文件内容
from enum import Enum


class REDIS_DB_URL(Enum):
        HOST = "47.103.27.246"  # 主机位置
        PORT = 6379  # 连接端口
        PASSWORD = "bupt"  # 连接密码
        DB = 0  # 所连数据库位置
