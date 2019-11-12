import json


class Serializer(object):
    @classmethod
    def serialize(cls, o: object) -> json:
        return json.dumps(o, default=lambda obj: cls.toDict(obj))

    @classmethod
    def toDict(cls, o: object) -> dict:
        d = o
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
    def deSerialize(cls, data: json, o: object) -> object:
        #TODO 反射
        jsonData = json.loads(data)
        if type(o).__name__ != jsonData["type"]:
            raise TypeError("object type: %s not match json type:%s" %
                            (type(o), jsonData["type"]))
        else:
            data = jsonData["data"]
            for k, v in data.items():
                setattr(o, k, v)
            return o
