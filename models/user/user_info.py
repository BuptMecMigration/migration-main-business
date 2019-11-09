# -*- coding: utf-8 -*-
from common.utils.time_utils import TimeUtils
from models.business.chain_info import ChainInfo


class UserToken(object):
    # 用户的相关token
    user_id: int
    service_id: int
    addr: {
        "user_ip": str,
        "user_port": str
    }

    @property
    def get_addr(self):
        return dict(self.addr)

    def __str__(self) -> str:
        return "the user's id is: %d, service is is: %d"%(self.user_id, self.service_id)

    def __init__(self, serviceId, ip, port) -> None:
        self.service_id = serviceId
        self.addr = {'user_ip': ip, 'user_port': port}


class UserBusiness(object):
    # 调用链相关信息
    is_migration: bool  # 迁移字段
    chain_offset: int  # 调用链位置
    data: str  # 传输数据
    mig_begin: float  # 传输时间戳

    def __init__(self, is_migration, offset, data) -> None:
        self.is_migration = is_migration
        self.chain_offset = offset
        self.data = data

    @property
    def get_mig_time(self):
        return TimeUtils.timestamp2time(self.mig_begin)

    @property
    def set_mig_time(self, new_time: float):
        self.mig_begin = new_time

    def __str__(self) -> str:
        return "当前调用链位置：%d" % self.chain_offset


# 服务所使用的真正实体
class UserService(object):

    # 用户相关token
    service_token: UserToken
    # 调用链执行信息
    service_bus: UserBusiness
    # 调用链基础信息
    service_chain: ChainInfo

    @property
    def set_migration_info(self, user_business: UserBusiness) -> None:
        self.service_bus = user_business

    @property
    def set_chain_info(self, chain_info: ChainInfo) -> None:
        self.service_chain = chain_info

    def __init__(self, user_token) -> None:
        self.service_token = user_token
