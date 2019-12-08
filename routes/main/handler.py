from flask import request
import requests

from models.business.chain_info import *
from models.user.user_info import *

from common.global_var import service_map
from common.utils import log
from threading import Lock

from concurrent.futures import ThreadPoolExecutor


class compute_handler(object):

    pool = ThreadPoolExecutor(1024)

    @classmethod
    def compute_us_func(cls, us: UserService):
        user_token, service_token = us.service_token.user_id, us.service_token.service_id
        cls.pool.submit(cls.handel_service, (user_token, service_token))
   
    @classmethod
    def mig_func(cls, us: UserService):
        cls.pool.submit(cls.handel_migration, (us))

    @classmethod
    def register_func(cls):
        service_map.register_us_func(cls.compute_us_func)
        service_map.register_migration_func(cls.mig_func)

    @classmethod 
    def handel_migration(cls, us: UserService):
        migration_maintainer.add_in_migration_us(us)

    @classmethod
    def handel_service(user_token: int, service_token: int):
        # 从offset恢复对应的服务
        is_In_map, us = service_map.get_user_service(user_token, service_token)
        if not is_In_map:
            log.logger.warn("not in service map")
            return

        offset, chain_length = us.service_bus.chain_offset, us.service_chain.num

        for i in range(offset,
                       chain_length):

            # 获取miniservice对应地址
            # 必须先处理完毕
            minServiceAddr, us_data = us.service_chain.mini_service[i], us.service_bus.data

            res = requests.post(minServiceAddr, data=us_data)

            # 从json文件中中获取data传输过来的data
            if res.status_code == 200:
                data = res.raw.read()
            if res.status_code != 200:
                log.logger.warn("receive non-200 return without doing anything ")
                # TODO re-try
                return

            us.lock_userService()
            is_migration = migration_maintainer.is_us_in_migration(us.service_token.service_id)
            if is_migration:
                # 需要处理migration逻辑,立即释放锁
                us.unlock_userService()
                log.logger.warn("migration begins")
                # Todo: 处理中断逻辑
                return

            # 更新data
            us.service_bus.data = data
            # 增加offset
            us.service_bus.chain_offset += 1
            us.unlock_userService()


class migration_maintainer(object):
    __lock=Lock()
    # 由于service_id唯一,使用Service作为key你说那你的话不能 
    __US_STATUS_MAP = {}

    @classmethod 
    def is_us_in_migration(cls,service_id:int):
        cls.__lock.acquire()
        output=True if service_id in cls.__US_STATUS_MAP else False
        cls.__lock.release()
        return output

    @classmethod
    def add_in_migration_us(cls,us: UserService):
        cls.__lock.acquire()
        us.service_bus.is_migration=True
        cls.__US_STATUS_MAP[us.service_token.service_id]=us
        cls.__lock.release()

    @classmethod
    def remove_us_by_service_id(cls,service_id: int):
        cls.__lock.acquire()
        if service_id in cls.__US_STATUS_MAP:
            cls.__US_STATUS_MAP[service_id].service_bus.is_migration=False
            del cls.__US_STATUS_MAP[service_id]
        cls.__lock.release()
