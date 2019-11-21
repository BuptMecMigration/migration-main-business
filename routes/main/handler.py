from flask import request
import requests
from models.business.chain_info import *
from models.user.user_info import *
from common.utils.logger import logger
from common.global_var import service_map
from common.utils.logger import logger

# TODO 传引用
def handel_service(user_token: int,service_token: int):
    # 从offset恢复对应的服务
    is_In_map,us=service_map.get_user_service(user_token,service_token)
    if not is_In_map:
        logger.warn("not in service map")
        return

    us.lock_userService()
    offset,chain_length=us.service_bus.chain_offset,us.service_chain.num
    us.unlock_userService()

    for i in range(offset,
                   chain_length):

        #获取miniservice对应地址
        # 必须先处理完毕  
        us.lock_userService()         
        minServiceAddr,us_data = us.service_chain.mini_service[i],us.service_bus.data
        res=requests.post(minServiceAddr, data=us_data)
        us.unlock_userService()

        # 从json文件中中获取data传输过来的data
        if res.status_code == 200:
            data = res.raw.read()
        if res.status_code != 200:
            logger.warn("receive non-200 return without doing anything ")
            return 

        us.lock_userService()
        is_migration=us.service_bus.is_migration
        us.unlock_userService()
        if is_migration:
            logger.warn("migration begins")
            #Todo : 处理中断逻辑
            return

        us.lock_userService()
        # 更新data
        us.service_bus.data= data
        #增加offset
        us.service_bus.chain_offset+=1
        us.unlock_userService()

