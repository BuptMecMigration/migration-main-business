from flask import jsonify, Blueprint, request

from common.utils.redis_utils import RedisUtil
from models.business.chain_info import ChainInfo
from models.user.user_info import UserToken

user_interface = Blueprint('user_interface', __name__)


# 接口：/user/sendTask
# 入参：serviceId, ip, port
# 出参：userId
@user_interface.route('/user/sendTask', methods=['POST'])
def user_job_handle():

    data = request.get_json()
    # 记录入参
    serviceId = data.get('serviceID')
    user_ip = data.get('ip')
    user_port = data('port')

    # 初始化一个redis连接
    redis_conn = RedisUtil

    # 生成userTokenn
    user_token = UserToken(serviceId, user_ip, user_port)

    # 分配ID
    # TODO
    id = 0
    user_token.user_id = id

    # token存redis

    # 根据serviceId获取redis中chainInfo并注入
    chain_info = redis_conn.get_redis_data(serviceId)


    # 初始化调用链状态并开始服务
    # TODO



    return jsonify({"user_id", id})


# 接口：/admin/addService
# 入参：serviceId, num, mini_service
# 出参：Flag
@user_interface.route('/admin/addService', method=['POST'])
def admin_add_service():

    data = request.get_json()
    serviceId = data.get('serviceID')
    num = data.get('num')
    mini_service = data.get('mini_service')

    # 初始化redis
    redis_conn = RedisUtil

    # 数据服务存入redis
    new_chain_info = ChainInfo(num, mini_service)
    RedisUtil.set_redis_data(serviceId, new_chain_info)

    # 可以加入reids操作成功与否判断条件
    # TODO

    return "service: %d is added now" % serviceId






