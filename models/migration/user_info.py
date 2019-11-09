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


class UserService(object):
    service_token: UserToken
    service_bus: UserBusiness
    service_chain: ChainInfo

    def __init__(self) -> None:
        super().__init__()

