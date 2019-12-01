from flask import request
import requests

from models.business.chain_info import *
from models.user.user_info import *

from common.global_var import service_map
from common import log

from concurrent.futures import ThreadPoolExecutor


class compute_handler(object):

    pool = ThreadPoolExecutor(1024)

    @classmethod
    def compute_us_func(cls, us: UserService):
        user_token, service_token = us.service_token.user_id, us.service_token.service_id
        cls.pool.submit(cls.handel_service, (user_token, service_token))
   
    @classmethod
    def mig_func(cls, us: UserService):
        pass

    @classmethod
    def register_func(cls):
        service_map.register_us_func(cls.compute_us_func)
        service_map.register_migration_func(cls.mig_func)

    @classmethod
    def handel_service(user_token: int, service_token: int):
        # 从offset恢复对应的服务
        is_In_map, us = service_map.get_user_service(user_token, service_token)
        if not is_In_map:
            log.logger.warn("not in service map")
            return

        us.lock_userService()
        offset, chain_length = us.service_bus.chain_offset, us.service_chain.num
        us.unlock_userService()

        for i in range(offset,
                       chain_length):

            # 获取miniservice对应地址
            # 必须先处理完毕
            us.lock_userService()
            minServiceAddr, us_data = us.service_chain.mini_service[i], us.service_bus.data
            us.unlock_userService()

            res = requests.post(minServiceAddr, data=us_data)

            # 从json文件中中获取data传输过来的data
            if res.status_code == 200:
                data = res.raw.read()
            if res.status_code != 200:
                log.logger.warn("receive non-200 return without doing anything ")
                # TODO re-try
                return

            us.lock_userService()
            is_migration = us.service_bus.is_migration
            if is_migration:
                # 需要处理migration逻辑,立即释放锁
                us.unlock_userService()
                log.logger.warn("migration begins")
                #Todo : 处理中断逻辑
                return

            # 更新data
            us.service_bus.data = data
            # 增加offset
            us.service_bus.chain_offset += 1
            us.unlock_userService()
