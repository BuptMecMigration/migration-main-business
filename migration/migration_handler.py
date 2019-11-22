# -*- coding: utf-8 -*-

"""
由于本模块已经使用us与data分离的设计模式，因此需要两个模块分别来对数据进行处理
模块A:
1）负责处理us信息的拷贝，并将其数据在本地恢复，主要使用TCP模式
    a）功能一：封装us，并查询对端的ip和port
    b）功能二：对us信息进行tcp发送，并注入service_map
2）用户接口启动迁移，启动对应数据的封装过程
模块B：
1）负责处理上一节点处转移过来的后续数据包信息，并调用相关的业务模块进行处理
2）这个部分使用rest还是tcp监听？
TODO：采用tcp是否很上一个模块功能可以复用？采用rest如何读取全局url信息（采用之前的redis存储方案？）
"""

import binascii
import json
import socket

#from common.global_var import service_map
from common.utils.redis_utils import RedisUtil
from common.utils.serialize import Serializer


"""
模块A的处理办法，直接调用并进行处理返回操作结果

@function: 在本节点处理用户全局状态，并转发后续结果
@param: userId：用户id
@return：success | fail
"""
def migration_sender(userId: int, serviceId: int) -> bool:
    # 处理用户全局map状态
    # 判断是否存在

    return_field = service_map.get_user_service(userId, serviceId)

    if not return_field[0]:
        # TODO 输出错误日志
        return False

    # 调换user_service的位置
    # service_map.remove_migration_service(userId, serviceId)
    # service_map.set_migration_service(return_field[1])

    # 转发用户后续请求，并调用相关状态

        # 读取另一节点上注册过的处理接口（包括ip和端口）

    # 如何获取一个分布式节点的rpc服务过程是难点？
    # @TODO

    return True


"""
@function: 接收用户发送过来的后续请求，并再对业务模块进行调用进行处理过程
@param: None
@return：Message
"""
def migration_receiver():
    # 将监听端口注册到某个地方

    # 开始监听过程

    # 接收用户请求并进行处理

    # 在本地map调整相关的用户状态，并向业务模块转发相应的操作
    return


"""
@function: 发送相关的请求进行关联
@param: None
@return: Msg
"""
def port_send(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect('localhost', 9000)
            s.sendall(Serializer.encode_socket_data(message))
            msg_len = int(binascii.hexlify(s.recv(4) or b'\x00'), 16)
            data = b''
            while msg_len > 0:
                tdat = s.recv(1024)
                data += tdat
                msg_len -= len(tdat)
        s.close()
    except Exception as e:
        print()


"""
@function: 发送相关的请求进行关联
@param: None
@return: Msg
"""
def port_receive(req, gs)-> object:
    data = b''
    # Our protocol is: first 4 bytes signify msg length.
    msg_len = int(binascii.hexlify(req.recv(4) or b'\x00'), 16)
    while msg_len > 0:
        tdat = req.recv(1024)
        data += tdat
        msg_len -= len(tdat)
    return Serializer.to_deserialize(data.decode(), gs) if data else None


"""
@function: 从redis读取所有节点信息存为一个map
@param: 某节点IP
@return: (ip, port)
"""
def get_target_peer(ip: str) -> str:
    peers = json.loads(RedisUtil.get_redis_data("peers"))
    for peer_ip in peers.key():
        if peer_ip == ip:
            return peers[peer_ip]
    return None


"""
@function: 将本节点信息存入dict中
@param: 某server的ip和port
@return: None
"""
def add_server_address(ip:str, port:int):
    peer_data = RedisUtil.get_redis_data("peers")
    dict = json.loads(peer_data)
    dict[ip]=port
    RedisUtil.set_redis_data("peers", json.dumps(dict))


if __name__ == '__main__':
    sstr = "10.1.1.1:9900,10.2.2.2:9901"
    peer = sstr.split(",")
    print(peer)