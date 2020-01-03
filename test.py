from common.global_var import service_map
from models.user.user_info import UserService, UserBusiness, UserToken
from models.business.chain_info import ChainInfo
from flask import Flask,jsonify,request
from routes.main.handler import compute_handler
import time

from common.utils.string_utils import StringUtils

token = UserToken(ip="0", port=0, service_id=0, user_id=1)
bus = UserBusiness(is_migration=False, offset=0, data=None)
chain = ChainInfo(num=2, mini_service={
    StringUtils.get_miniservice_key(0): "http://127.0.0.1:5000/test_addr0",
    StringUtils.get_miniservice_key(1): "http://127.0.0.1:5000/test_addr1"})
us=UserService(user_token=token,service_bus=bus,service_chain=chain)

app = Flask(__name__)

@app.route("/test_addr0",methods=["GET", "POST"])
def test_addr0():
    time.sleep(10)
    return jsonify({"answer":1})

@app.route("/test_addr1",methods=["GET", "POST"])
def test_addr1():
    request.json["answer"] += 2
    return request.json

@app.route("/")
def active():
    compute_handler.register_func()
    service_map.set_user_service(us)

    return "ok"

@app.route("/remove_func")
def test_remove_us_func():
    if service_map.remove_user_service(1,0):
        us.service_bus.chain_offset=0
        return "ok"
    return "!ok"

@app.route("/migration_call")
def test_migration_map_func():
    if service_map.set_migration_service(us):
        return "ok"
    return "!ok"

if __name__ == '__main__':
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
