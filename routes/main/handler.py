from flask import request
import requests
from models.business.chain_info import *
from models.user.user_info import *
from common.utils.logger import logger

# TODO 传引用
def handel_migration(userService: UserService):
    # 从offset恢复对应的服务
    offset=userService.service_bus.chain_offset
    for i in range(offset,
                   userService.service_chain.num):
        #获取miniservice对应地址           
        minServiceAddr = userService.service_chain.mini_service[i]
        res=requests.post(minServiceAddr, data=userService.service_bus.data)
        # 从json文件中中获取data传输过来的data
        if res.status_code == 200:
            data = res.raw.read()
            userService.service_bus.data= data
            userService.service_bus.chain_offset+=1
            # 需要迁移,处理中断
            if userService.service_bus.is_migration:
                logger.warn("migration begins")
                #Todo : 处理中断逻辑
                return

        if res.status_code != 200:
            logger.warn("receive non-200 return without doing anything ")
            return 
