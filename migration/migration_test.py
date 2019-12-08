import time

from common.utils.serialize_utils import Serializer
from models.user.user_info import UserToken, UserService

import cloudpickle
import pickle

if __name__ == '__main__':
    uk = UserToken(ip='0.0.0.0', port='9999', user_id=1, serviceId=1277)
    us = UserService(user_token=uk)
    # print(type(globals()['UserToken']))
    # print(globals()['UserToken'])
    # temp = Serializer.serialize(uk)
    # print(temp)
    # print(type(temp))
    temp = cloudpickle.dumps(us)
    print(temp)
    print(type(temp))
    recover = pickle.loads(temp)
    print(recover)
    print(type(recover))
    print(type(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
