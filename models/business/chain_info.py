# -*- coding: utf-8 -*-


# 服务调用链信息,存在配置中心中,在迁移时一并发送节省时间
# 本质是配置中心信息的拷贝
from common.utils.string_utils import StringUtils


class ChainInfo(object):
    '''
    总的微服务的数量
    @ num: int
    - index->int: addr->str
    - service_addr 是 service的URI
    - eg: "mini_service": {
         "index_int(0)": "service_addr0",
         "index_int(1)": "service_addr1"
     }
    - mini_service: dict
    '''

    @property
    def service_addr(self, index: int):
        return self.mini_service.get(StringUtils.get_miniservice_key(index))

    def __init__(self, num: int, mini_service: dict) -> None:
        self.num = num
        self.mini_service = mini_service

    def __repr__(self) -> str:
        return repr((self.num, self.mini_service))

