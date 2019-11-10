import json


class Serializer(object):
    @classmethod
    def serialize(cls, o: object) -> json:
        return json.dumps(o, default=lambda obj: {
            "type": type(obj).__name__,
            "data": obj.__dict__
        }
        )

    # 反序列化,需要检查当前类型
    # 目前简单的重载了类数据,之后可以考虑根据type动态生成对象
    @classmethod
    def deSerialize(cls, data: json, o: object) -> object:
        jsonData = json.loads(data)
        if type(o).__name__ != jsonData["type"]:
            raise TypeError("object type: %s not match json type:%s" %
                            (type(o), jsonData["type"]))
        else:
            data = jsonData["data"]
            for k, v in data.items():
                setattr(o, k, v)
            return o
