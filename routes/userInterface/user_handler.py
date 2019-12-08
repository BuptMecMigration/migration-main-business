from flask import jsonify, Blueprint, request
import requests

from common.global_var import service_map
from common.utils.redis_utils import RedisUtil
from common.utils.token_utils import Token
from migration.migration_handler import migration_sender
from models.business.chain_info import ChainInfo
from models.user.user_info import UserToken, UserService, UserBusiness

user_interface = Blueprint('user_interface', __name__)


# 接口：/user/sendTask
# 入参：serviceId, ip, port, req_data
# 出参：userId
@user_interface.route('/user/sendTask', methods=['POST'])
def user_job_handle():

    data = request.get_json()
    # 记录入参
    serviceId = data.get('serviceID')
    user_ip = data.get('ip')
    user_port = data('port')
    req_data = data('req_data')

    # 生成userToken，分配id
    id = Token.gen_service_token()
    user_token = UserToken(serviceId=serviceId, ip=user_ip, port=user_port, user_id=id)

    # token存redis
    RedisUtil.set_redis_data(user_token.user_id, user_token)

    # 根据serviceId获取redis中chainInfo并注入
    # 这里的chain_data应该对应内容为一个Chain_Info类
    chain_data = RedisUtil.get_redis_data("serviceId_%d" % serviceId)
    chain_info = ChainInfo(chain_data["num"], chain_data["mini_service"])

    # 初始化调用链状态
    business_data = UserBusiness(False, 0, req_data)

    # 封装UserService
    user_service = UserService(user_token=user_token)
    user_service.set_migration_info(business_data)
    user_service.set_chain_info(chain_data)

    # 向内部URL发送一个带有UserService信息的请求
    url = chain_info.service_addr(business_data.chain_offset)
    req = requests.post(url, user_service)

    return jsonify({"user_id": id, "redirect_result": req})


# 接口：/user/startMigration
# 入参：userId, serviceID, ip, port
# 出参：Flag
@user_interface.route('/user/startMigration', methods=['POST'])
def user_migration_handle():

    data = request.get_json()
    userId = data.get('userId')
    serviceId = data.get('serviceId')
    ip = data.get('ip')
    port = data.get('port')

    # 修改redis中用户的ip及port信息
    token = RedisUtil.get_redis_data(userId)
    RedisUtil.set_redis_data(userId, UserToken(user_id=userId, serviceId=token["serviceID"], ip=ip, port=port))

    # 后续迁移处理信息部分UserBusiness的flag都变成True
    returnField = service_map.get_user_service(userId, serviceId)
    if not returnField[0]:
        return "You service is not recorded"
    # 并且交给迁移转发模块进行处理，不在本地进行处理
    if migration_sender(userId=userId, serviceId=serviceId, flag=0, ip=ip):
        return "Operate migration process fail!"

    return "Migration is started, new ip: %s, new port: %d" % (ip, port)


# 接口：/admin/addService
# 入参：serviceId, num, mini_service
# 出参：Flag
@user_interface.route('/admin/addService', methods=['POST'])
def admin_add_service():

    data = request.get_json()
    serviceId = data.get('serviceId')
    num = data.get('num')
    mini_service = data.get('mini_service')

    # 数据服务存入redis
    new_chain_info = ChainInfo(num, mini_service)
    RedisUtil.set_redis_data("serviceId_%d" % serviceId, new_chain_info)

    return "service: %d is added now" % serviceId


# test_redis_read
@user_interface.route('/test/redis_get', methods=['POST'])
def test_redis_read():

    data = request.get_json()
    key = data.get('key')
    chain = RedisUtil.get_redis_data(key)
    return "get: %s" % chain


# test_redis_write
@user_interface.route('/test/redis_set', methods=['POST'])
def test_redis_write():

    data = request.get_json()
    key = data.get('key')
    val = data.get('val')
    RedisUtil.set_redis_data(key, val)
    return "set: %s" % val


# test_function_1
@user_interface.route('/test/function_1', methods=['POST'])
def test_business_func1():

    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func1_part_"
    return data_str


# test_function_2
@user_interface.route('/test/function_2', methods=['POST'])
def test_business_func2():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func2_part_"
    return data_str


# test_function_3
@user_interface.route('/test/function_3', methods=['POST'])
def test_business_func3():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func3_part_"
    return data_str


# test_function_4
@user_interface.route('/test/function_4', methods=['POST'])
def test_business_func4():
    data = request.get_json()
    data_str = data.get('test_string')
    data_str += "this_is_func4_part!"
    return data_str


# get_result_function
@user_interface.route('/test/get_function', methods=['POST'])
def get_function():
    # us =
    us = UserService()
    return us.service_bus.data