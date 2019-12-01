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
import socketserver
import threading
import time

from common.code import TRIES_MAXIMUM
from common.global_var import service_map
from common.utils.logger_utils import Logger
from common.utils.redis_utils import RedisUtil
from common.utils.serialize_utils import Serializer
from migration.Message import Message, MsgFlag
from models.user.user_info import UserService

log = Logger('../../logs/all.log', level='info')
log_error = Logger('../../logs/error.log', level='error')


"""
模块A的处理办法，直接调用并进行处理返回操作结果

@function: 在本节点处理用户全局状态，并转发后续结果
@param: userId：用户id
@return：success | fail
"""
def migration_sender(userId: int, flag: bool, serviceId: int, ip: str) -> bool:

    # 处理用户全局map状态
    # 判断是否存在
    return_field = service_map.get_user_service(userId, serviceId)

    if not return_field[0]:
        # 输出错误日志
        log.logger.info('[访问错误]: 用户未注册，请注册节点后再进行迁移操作')
        return False
    us = return_field[1]
    service_map.set_user_service(return_field[1].setflag(True))

    # 读取另一节点上注册过的处理接口（包括ip和端口）
    port = get_target_peer(ip)
    if port == -1:
        return False

    # 调用TCP模块，转发用户后续请求
    if not port_send(us, flag, ip, port):
        return False

    return True


"""
@function: 接收用户发送过来的后续请求，并再对业务模块进行调用进行处理过程
@param: None
@return：Message
"""
def migration_receiver(port: int):

    def start_worker(workers, worker):
        log.logger.info('[运行时]: TCPServer已在本地: {} 开始监听'.format(port))
        workers.append(threading.Thread(target=worker, daemon=True))
        workers[-1].start()

    # 将监听端口注册到某个地方，这个地方最好写成全局IP
    workers = []
    server = ThreadedTCPServer(('localhost', port), TCPHandler)
    # 开始监听过程
    start_worker(workers, server.serve_forever)
    # 接收用户请求并进行处理
    # 在本地map调整相关的用户状态，并向业务模块转发相应的操作
    # 这部分操作写在TCPserver的handler里
    return


"""
@function: 发送相关的请求进行关联
@param: None
@return: Msg
"""
def port_send(data: object, flag:int, ip: str , port: int) -> bool:

    tries_left = int(TRIES_MAXIMUM)

    if tries_left <= 0:
        # 日志模块写入重试失败问题记录
        return False

    while tries_left > 0:
        try:
            message = ''
            if flag == 0:
                message = Message(MsgFlag.MsgUsRecover, data)
            if flag == 1:
                message = Message(MsgFlag.MsgUsDataRecover, data)
            with socket.create_connection((ip, port)) as s:
                s.sendall(Serializer.pickle_serialize(message))
        except Exception as e:
            tries_left -= 1
            time.sleep(1)
            if tries_left <= 0:
                return False
        else:
            return True


"""
@function: 发送相关的请求进行关联
@param: None
@return: Msg
"""
def port_receive(req: bytes)-> object:
    data = b''
    # 前4 Bytes代表数据长度
    msg_len = int(binascii.hexlify(req.recv(4) or b'\x00'), 16)
    while msg_len > 0:
        tdat = req.recv(1024)
        data += tdat
        msg_len -= len(tdat)
    return Serializer.pickle_deserialize(data) if data else None


"""
@function: 从redis读取所有节点信息存为一个map
@param: 某节点IP
@return: (ip, port)
"""
def get_target_peer(ip: str) -> int:
    peers = json.loads(RedisUtil.get_redis_data("peers"))
    for peer_ip in peers.key():
        if peer_ip == ip:
            return peers[peer_ip]
    return -1


"""
@function: 将本节点信息存入dict中
@param: 某server的ip和port
@return: None
"""
def add_server_address(ip: str, port: int):
    peer_data = RedisUtil.get_redis_data("peers")
    dict = json.loads(peer_data)
    dict[ip] = port
    RedisUtil.set_redis_data("peers", json.dumps(dict))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
        the TCP Server class to support the data receive.
        the handler is the method we write to receive different type of data.
        author: jqliu_bupt@163.com
    """
    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


"""
重写TCP_handler处理相关逻辑
"""
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # 接收相关消息恢复处理, gs为相关map处理过程
        try:
            message = Serializer.read_all_from_socket(self.request)
        except Exception as e:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("get exception from socket receive part: {} and time is {}".format(e, cur_time))
            return

        if not isinstance(message, Message):
            # 输出日志
            return

        action = int(message.msg_flag)
        us = message.data

        if not isinstance(us, UserService):
            # 输出日志
            return

        if action == MsgFlag.MsgUsRecover:
            # 处理us信息
            service_map.set_user_service(us)
        if action == MsgFlag.MsgUsDataRecover:
            # 处理后续转发消息, 需要接口
            service_map.set_user_service(us)
        # 关闭接口
        self.request.shutdown(2)
        self.request.close()


if __name__ == '__main__':
    sstr = "10.1.1.1:9900,10.2.2.2:9901"
    peer = sstr.split(",")
    print(peer)