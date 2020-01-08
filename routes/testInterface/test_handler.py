from flask import Blueprint, request, jsonify

from common.utils.redis_utils import RedisUtil
from common.utils.string_utils import StringUtils
from migration.migration_handler import port_send
from models.business.chain_info import ChainInfo
from models.user.user_info import UserService, UserToken, UserBusiness

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
    return jsonify("test_string", data_str)


# test_function_2
@test_interface.route('/function_2', methods=['POST'])
def test_business_func2():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func2_part_"
    return data_str


# test_function_3
@test_interface.route('/function_3', methods=['POST'])
def test_business_func3():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func3_part_"
    return data_str


# test_function_4
@test_interface.route('/function_4', methods=['POST'])
def test_business_func4():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func4_part!"
    return data_str


# get_result_function
@test_interface.route('/test_tcp_receiver', methods=['POST'])
def get_function():
    data = request.get_json()
    user_id = data.get('userId')
    service_id = data.get('serviceId')

    token = UserToken(ip="0", port=0, service_id=service_id, user_id=user_id)
    bus = UserBusiness(is_migration=False, offset=0, data=None)
    chain = ChainInfo(num=2, mini_service={
        StringUtils.get_miniservice_key(0): "http://127.0.0.1:5000/test_addr0",
        StringUtils.get_miniservice_key(1): "http://127.0.0.1:5000/test_addr1"})
    us = UserService(user_token=token, service_bus=bus, service_chain=chain)

    port_send(us, 0, '0.0.0.0', 9900)

    return "发送成功"

