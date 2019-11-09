from flask import jsonify, Blueprint, request

from models.user.user_info import UserToken

user_interface = Blueprint('user_interface', __name__)


# 接口：/user/sendTask
# 入参：serviceId, ip, port
# 出参：userId
@user_interface.route('/user/sendTask', methods=['GET'])
def user_job_handle():

    # 记录入参
    serviceId = request.args['serviceID']
    user_ip = request.args['ip']
    user_port = request.data['port']

    # 生成userTokenn
    user_token = UserToken(serviceId, user_ip, user_port)

    # 分配ID
    # TODO
    id = 0
    user_token.user_id = id

    # token存redis

    # 根据serviceId获取redis中chainInfo并注入
    # TODO

    # 初始化调用链状态并开始服务
    # TODO

    return jsonify({"user_id", id})