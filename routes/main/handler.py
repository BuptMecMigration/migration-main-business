from flask import request
import requests
from models.business.chain_info import *
from models.user.user_info import *


def handel_migration(userService: UserService):
    # 从offset恢复对应的服务
    for i in range(userService.service_bus.chain_offset,
                   userService.service_chain.num):
        #获取miniservice对应地址           
        minServiceAddr = userService.service_chain.mini_service[i]
        respose=requests.post(minServiceAddr, data=userService.service_bus.data)
        # 从json文件中中获取data传输过来的data
        respose.
        data = request.file['data']
