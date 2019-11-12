# -*- coding: utf-8 -*-
import json
import pickle


class StringUtils(object):

    # 从服务链信息中mini_service获取字符串转化为ip和端口
    @classmethod
    def addr2socketPair(cls, addr: str) -> dict:
        result = addr.split(":")
        return {"ip": result[0], "port": result[1]}

    # 组装获取mini_service序列的key值
    @classmethod
    def get_miniservice_key(cls, offset: int) -> str:
        return "index_int(%d)" % offset
