# -*- coding: utf-8 -*-
from common.utils.time_utils import TimeUtils
from models.business.chain_info import ChainInfo


class UserToken(object):
    """
        用户的相关token
        user_id: int
        service_id: int
        addr: {
            "user_ip": str,
            "user_port": str
        }
    """
    @property
    def get_addr(self):
        return dict(self.addr)

    def __init__(self,  *, ip, port, service_id: int, user_id: int) -> None:
        self.user_id = user_id
        self.service_id = service_id
        self.addr = {'user_ip': ip, 'user_port': port}

    def __str__(self) -> str:
        return "the user's id is: %d, service is is: %d" % (self.user_id, self.service_id)


class UserBusiness(object):

    '''
     调用链相关信息
    is_migration: bool   ->迁移字段
    chain_offset: int   ->调用链位置
    data: str   ->传输数据
    mig_begin: float  -> 迁移时间戳
    '''

    def __init__(self, *, is_migration, offset, data) -> None:
        self.is_migration = is_migration
        self.chain_offset = offset
        self.data = data

    @property
    def get_mig_time(self):
        return TimeUtils.timestamp2time(self.mig_begin)

    def set_mig_time(self, new_time: float):
        self.mig_begin = new_time

    def __str__(self) -> str:
        return "当前调用链位置：%d" % self.chain_offset


# 服务所使用的真正实体
class UserService(object):

    """
        - 用户相关token
            - service_token: UserToken
        - 调用链执行信息
            - service_bus: UserBusiness
        - 调用链基础信息
            - service_chain: ChainInfo
    """

    def set_migration_info(self, user_business: UserBusiness) -> None:
        self.service_bus = user_business

    def set_chain_info(self, chain_info: ChainInfo) -> None:
        self.service_chain = chain_info

    @property
    def get_migration_info(self):
        return self.service_bus

    @property
    def get_chain_info(self):
        return self.service_chain

    def __init__(self, *, user_token: UserToken, service_bus: UserBusiness, service_chain: ChainInfo) -> None:
        self.service_token: UserToken = user_token
        self.service_bus: UserBusiness = service_bus
        self.service_chain: ChainInfo = service_chain
