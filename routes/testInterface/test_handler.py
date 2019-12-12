from flask import Blueprint, request

from common.utils.redis_utils import RedisUtil
from models.user.user_info import UserService

test_interface = Blueprint('test_interface', __name__)


@test_interface.route('/')
def for_test():
    return "This is test interface!"


# 以下接口为测试使用
# test_redis_read
@test_interface.route('/redis_get', methods=['POST'])
def test_redis_read():

    data = request.get_json()
    key = data.get('key')
    chain = RedisUtil.get_redis_data(key)
    return "get the type of the return object: {} and its msg: {}".format(type(chain), chain.__str__())


# test_redis_write
@test_interface.route('/redis_set', methods=['POST'])
def test_redis_write():

    data = request.get_json()
    key = data.get('key')
    val = data.get('val')
    RedisUtil.set_redis_data(key, val)
    return "set: %s" % val


# test_function_1
@test_interface.route('/function_1', methods=['POST'])
def test_business_func1():

    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func1_part_"
    return data_str


# test_function_2
@test_interface.route('=/function_2', methods=['POST'])
def test_business_func2():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func2_part_"
    return data_str


# test_function_3
@test_interface.route('=/function_3', methods=['POST'])
def test_business_func3():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func3_part_"
    return data_str


# test_function_4
@test_interface.route('=/function_4', methods=['POST'])
def test_business_func4():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func4_part!"
    return data_str


# get_result_function
@test_interface.route('=/get_function', methods=['POST'])
def get_function():
    # us =
    us = UserService()
    return us.service_bus.data

