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
    user_port = data.get('port')
    req_data = data.get('req_data')

    # 生成userToken，分配id
    id = Token.gen_service_token()
    user_token = UserToken(service_id=serviceId, ip=user_ip, port=user_port, user_id=id)

    # token存redis
    RedisUtil.set_redis_data(user_token.user_id, user_token)

    # 根据serviceId获取redis中chainInfo并注入
    # 这里的chain_data应该对应内容为一个Chain_Info类
    chain_data = RedisUtil.get_redis_data("serviceId_%d" % serviceId)
    # chain_info = ChainInfo(chain_data["num"], chain_data["mini_service"])

    # 初始化调用链状态
    business_data = UserBusiness(is_migration=False, offset=0, data=req_data)

    # 封装UserService
    user_service = UserService(user_token=user_token, service_bus=business_data, service_chain=chain_data)

    # 这部分直接调用相关的map内置函数去处理对应的业务逻辑
    if not service_map.set_user_service(user_service):
        return "该业务已经存在，业务异常"
    # compute_handler.compute_us_func(user_service) 该业务已经直接启动

    return jsonify({"user_id": id, "redirect_result": "your target ip is: {}:{} now".format(user_ip, user_port)})


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
    RedisUtil.set_redis_data(userId, UserToken(user_id=userId, service_id=token["serviceID"], ip=ip, port=port))

    # 后续迁移处理信息部分UserBusiness的flag都变成True
    # 并且交给迁移转发模块进行处理，不在本地进行处理
    if not migration_sender(userId=userId, serviceId=serviceId, flag=0, ip=ip):
        return "Operate migration process fail!"

    return "Migration is started, new ip: %s, new port: %d" % (ip, port)

# 接口：/user/getResult
# 入参：userId, serviceId
# 出参：返回data
@user_interface.route('/user/getResult', methods=['POST'])
def user_get_result():

    data = request.get_json()
    userId = data.get('userId')
    serviceId = data.get('serviceId')

    if not service_map.is_us_success(userId, serviceId):
        return "业务处理失败"

    msg = service_map.pop_success_user(userId, serviceId)
    return msg[-1].service_bus.data


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
