# -*- coding: utf-8 -*-
import time


class TimeUtils(object):

    @classmethod
    def time2timestamp(cls, time: str) -> float:
        # 转换成时间数组
        timeArray = time.strptime(time, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        return  time.mktime(timeArray)

    @classmethod
    def timestamp2time(cls, timestamp: float) -> str:
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(eg: 2016-05-05 20:28:54)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_local)
