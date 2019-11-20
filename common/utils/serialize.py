import binascii
import json
from typing import (
    Iterable, NamedTuple, Dict, Mapping, Union, get_type_hints, Tuple,
    Callable)


class Serializer(object):
    @classmethod
    def serialize(cls, o: object) -> json:
        return json.dumps(o, default=lambda obj: cls.toDict(obj))

    @classmethod
    def toDict(cls, o: object) -> dict:
        d=o
        if not isinstance(o, (dict, list, tuple, str, int, float, bool)):
            d = {"serialized_tag_type": type(o).__name__,
                 "serialized_tag_data": o.__dict__}
            for k, v in d["serialized_tag_data"].items():
                if k == "serialized_tag_type" or k=="serialized_tag_data":
                    raise Exception("must not have serialized_tag_type,serialized_tag_data as key")
                d["serialized_tag_data"][k] = cls.toDict(v)
        return d

    # 反序列化,需要检查当前类型
    # 目前简单的重载了类数据,之后可以考虑根据type动态生成对象
    @classmethod
    def deSerialize(cls, data: json) -> object:
        # TODO 反射
        jsonData = json.loads(data)
        return cls.gen_obj(jsonData)

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
    def encode_socket_data(cls, data: object) -> bytes:
        """Our protocol is: first 4 bytes signify msg length."""

        def int_to_8bytes(a: int) -> bytes:
            return binascii.unhexlify(f"{a:0{8}x}")

        to_send = cls.to_serialize(data).encode()
        return int_to_8bytes(len(to_send)) + to_send
