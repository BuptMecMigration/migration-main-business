# -*- coding: utf-8 -*-
# 对内部服务的入口进行注册
from enum import Enum


class MAIN_PROCESS_URL(Enum):
    start_service = "/xxx/xxx"  # 发送主要的URL进行处理


class DISPATCH_URL(Enum):
    base_service = "/xxx/xxx"  # 结果转发的主要URL
