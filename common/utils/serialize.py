import binascii
import pickle
import json
import pickle
from typing import (
    Iterable, NamedTuple, Dict, Mapping, Union, get_type_hints, Tuple,
    Callable)

import cloudpickle


class Serializer(object):
    @classmethod
    def serialize(cls, o: object) -> bytes:
        return pickle.dumps(o)


    # 反序列化,需要检查当前类型
    # 目前简单的重载了类数据,之后可以考虑根据type动态生成对象
    @classmethod
    def deSerialize(cls, data: bytes) -> object:
        return pickle.loads(data)

    @classmethod
    def gen_obj(cls, d:dict)->object:
        if "serialized_tag_type" in d:
            if d["serialized_tag_type"] not in globals():
                raise TypeError("object type: %s not implemented" % (d["serialized_tag_type"]))
            
            obj=globals()[d["serialized_tag_type"]]()
            for k, v in d["serialized_tag_data"].items():
                setattr(obj,k,cls.gen_obj(v))
            return obj
        else:
            return d

    @classmethod
    def to_serialize(cls, obj) -> str:
        """NamedTuple-flavored serialization to JSON."""

        def contents_to_primitive(o):
            if hasattr(o, '_asdict'):
                o = {**o._asdict(), '_type': type(o).__name__}
            elif isinstance(o, (list, tuple)):
                return [contents_to_primitive(i) for i in o]
            elif isinstance(o, bytes):
                return binascii.hexlify(o).decode()
            elif not isinstance(o, (dict, bytes, str, int, type(None))):
                raise ValueError(f"Can't serialize {o}")
            if isinstance(o, Mapping):
                for k, v in o.items():
                    o[k] = contents_to_primitive(v)
            return o

        return json.dumps(contents_to_primitive(obj), sort_keys=True, separators=(',', ':'))

    @classmethod
    def to_deserialize(cls, serialized: str, gs: dict) -> object:
        """NamedTuple-flavored serialization from JSON."""

        def contents_to_objs(o):
            if isinstance(o, list):
                return [contents_to_objs(i) for i in o]
            elif not isinstance(o, Mapping):
                return o

            _type = gs[o.pop('_type', None)]
            bytes_keys = {
                k for k, v in get_type_hints(_type).items() if v == bytes}

            for k, v in o.items():
                o[k] = contents_to_objs(v)

                if k in bytes_keys:
                    o[k] = binascii.unhexlify(o[k]) if o[k] else o[k]

            return _type(**o)

        return contents_to_objs(json.loads(serialized))

    @classmethod
    def pickle_serialize(cls, data: object) -> bytes:
        """use pickle way to serialize the data"""
        # 后续代码可以抽离出来再次重用
        # https://github.com/cloudpipe/cloudpickle
        return cloudpickle.dumps(data)

    @classmethod
    def pickle_deserialize(cls, data: bytes) -> object:
        return pickle.loads(data)

    @classmethod
    def encode_socket_data(cls, data: object) -> bytes:
        """Our protocol is: first 4 bytes signify msg length."""

        def int_to_8bytes(a: int) -> bytes:
            return binascii.unhexlify(f"{a:0{8}x}")

        to_send = cls.pickle_serialize(data)
        return int_to_8bytes(len(to_send)) + to_send

    @classmethod
    def read_all_from_socket(cls, req) -> object:
        data = b''
        # Our protocol is: first 4 bytes signify msg length.
        msg_len = int(binascii.hexlify(req.recv(4) or b'\x00'), 16)

        while msg_len > 0:
            tdat = req.recv(1024)
            data += tdat
            msg_len -= len(tdat)

        return cls.pickle_deserialize(data) if data else None
