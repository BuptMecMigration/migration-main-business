from flask import request
import requests
from models.business.chain_info import *
from models.user.user_info import *
from common.utils.logger import logger
from common.global_var import global_var

global_var.get_user_service()
# TODO 传引用
def handel_migration(userServiceToken: int):
    # 从offset恢复对应的服务
    is_In_map,us=global_var.get_user_service(userServiceToken)
    if not is_In_map:
        return
    offset=us.service_bus.chain_offset

    for i in range(offset,
                   us.service_chain.num):
        #获取miniservice对应地址           
        minServiceAddr = us.service_chain.mini_service[i]

        # 每次重新请求一下最新的信息(可能被迁移走了)
        is_In_map,new_us=global_var.get_user_service(userServiceToken)
        if not is_In_map:
            #TODO 是否要考虑一下其中的情况  
            return

        res=requests.post(minServiceAddr, data=is_In_map,us=new_us.service_bus.data)
        # 从json文件中中获取data传输过来的data
        if res.status_code == 200:
            data = res.raw.read()

        is_In_map,new_us=global_var.get_user_service(userServiceToken)
        if not is_In_map:
            #TODO  
            return
        # 从信息中获得需要迁移
        if new_us.service_bus.is_migration:
                logger.warn("migration begins")
                #Todo : 处理中断逻辑
                return
        # 更新data
        new_us.service_bus.data= data
        #增加offset
        new_us.service_bus.chain_offset+=1

        if res.status_code != 200:
            logger.warn("receive non-200 return without doing anything ")
            return 
