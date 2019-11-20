# -*- coding: utf-8 -*-


"""
@function: 在本节点处理用户全局状态，并转发后续结果
@param: userId：用户id
@return：success | fail
"""
import binascii
import socket

from common.utils.serialize import Serializer


def migration_sender(userId: int) -> bool:
    # 处理用户全局map状态

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

