from flask import request
import requests

from common.utils.logger_utils import print2file
from migration.migration_handler import get_target_peer, port_send
from models.business.chain_info import *
from models.user.user_info import *

from common.global_var import service_map
from common.utils import log
from threading import Lock

from concurrent.futures import ThreadPoolExecutor


class compute_handler(object):

    pool = ThreadPoolExecutor(max_workers=1024)

    @classmethod
    def compute_us_func(cls, us: UserService):

        print("begin compute")

        user_token, service_token = us.service_token.user_id, us.service_token.service_id
        cls.pool.submit(cls.handel_service, user_token, service_token)
   
    @classmethod
    def mig_func(cls, us: UserService):
        print("add to migration pool")
        cls.pool.submit(cls.handel_migration, us)

    @classmethod
    def register_func(cls):
        service_map.register_us_func(cls.compute_us_func)
        service_map.register_migration_func(cls.mig_func)

    @classmethod 
    def handel_migration(cls, us: UserService):
        print("handel migration")
        migration_maintainer.add_in_migration_us(us)

    @classmethod
    # checked!
    def handel_service(cls, user_token: int, service_token: int):
        # 从offset恢复对应的服务
        is_In_map, us = service_map.get_user_service(user_token, service_token)
        if not is_In_map:
            log.logger.warn("not in service map")
            return

        offset, chain_length = us.service_bus.chain_offset, us.service_chain.num

        print("chain_length: ", chain_length)

        # print("get user_service", us.__dict__)
        # print2file("point")
        print("current offset is :", offset)
        for i in range(offset,
                       chain_length):
            print("process sub-process: ", i)
            # 获取miniservice对应地址
            # 必须先处理完毕
            minServiceAddr, us_data = us.service_chain.mini_service[StringUtils.get_miniservice_key(i)], \
                                      us.service_bus.data
            # print("sub-process", i, " minServiceAddr:", minServiceAddr, " data: ", us_data)
            print("sub-process", i, " minServiceAddr:", minServiceAddr)

            # print2file("point-2")
            # print2file("point-1: type:{} len:{}".format(type(us_data), us_data.keys()))
            # print2file(len(us_data["process_file"]))
            print2file("point-2-1")
            # print2file(us_data)
            res = requests.post(minServiceAddr, json=us_data)
            print2file("point-3")
            # 从json文件中中获取data传输过来的data
            if res.status_code == 200:
                data = res.json()
                # print(bytes(data["process_file"], encoding='utf-8'))
                # print("the received data is ", data)
            if res.status_code != 200:
                log.logger.warn("receive non-200 return without doing anything ")
                # TODO re-try
                return

            is_migration = (service_map.get_migration_service(user_token, service_token)[0])
            # print2file("point-6 {}".format(is_migration))
            if is_migration:
                migration_data = service_map.get_migration_service(user_token, service_token)[1]
                migration_data.service_bus.chain_offset = us.service_bus.chain_offset
                # 需要处理migration逻辑,立即释放锁
                log.logger.warn("migration begins")
                # 直接停止并将service_map里的数据删除
                # 读取另一节点上注册过的处理接口（包括ip和端口）
                port = get_target_peer(migration_data.service_bus.target_ip)
                print("port: %d" % port)
                if port == -1:
                    log.logger.info('[服务器错误]: 服务器获取ip对应端口失败')
                    return False
                print("get target port {} for ip: {}".format(port, migration_data.service_bus.target_ip))
                print2file("start")
                # 调用TCP模块，转发用户后续请求
                if not port_send(migration_data,
                                 migration_data.service_bus.migration_flag,
                                 migration_data.service_bus.target_ip,
                                 port):
                    return False
                service_map.remove_migration_service(user_token, service_token)
                return

            # print2file("point-4")
            # 更新data
            us.service_bus.data = data
            # 增加offset
            us.service_bus.chain_offset += 1

        print("process done!")
        service_map.add_success_us(user_token, service_token)


class migration_maintainer(object):
    __lock = Lock()
    # 由于service_id唯一,使用Service作为key你说那你的话不能 
    __US_STATUS_MAP = {}

    @classmethod 
    def is_us_in_migration(cls, user_token: int):
        cls.__lock.acquire()
        output = True if user_token in cls.__US_STATUS_MAP else False
        cls.__lock.release()
        return output

    @classmethod
    def add_in_migration_us(cls, us: UserService):
        cls.__lock.acquire()
        us.service_bus.is_migration = True
        cls.__US_STATUS_MAP[us.service_token.service_id] = us
        cls.__lock.release()

    @classmethod
    def remove_us_by_service_id(cls, service_id: int):
        cls.__lock.acquire()
        if service_id in cls.__US_STATUS_MAP:
            cls.__US_STATUS_MAP[service_id].service_bus.is_migration = False
            del cls.__US_STATUS_MAP[service_id]
        cls.__lock.release()
