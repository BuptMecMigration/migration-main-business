from typing import NamedTuple


class MsgFlag:
    """
    the class we use to map different kinds of messages we want to send to their id.
    """
    MsgUsRecover = 0
    MsgUsDataRecover = 1
    # 可扩展信息

    num2flag = {
        '0': 'MsgUsRecover',
        '1': 'MsgUsDataRecover'
    }


class Message(NamedTuple):
    """
    the class we use to transfer the data to the target port.
    """
    msg_flag: int
    data: object
