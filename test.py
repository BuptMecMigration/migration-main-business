from common.global_var import service_map
from models.user.user_info import UserService, UserBusiness, UserToken
from models.business.chain_info import ChainInfo
from flask import Flask,jsonify,request
from routes.main.handler import compute_handler

token = UserToken(ip="0", port=0, service_id=0, user_id=1)
bus = UserBusiness(is_migration=False, offset=0, data=None)
chain = ChainInfo(num=2, mini_service={
    0: "http://127.0.0.1:5000/test_addr0",
    1: "http://127.0.0.1:5000/test_addr1"})
us=UserService(user_token=token,service_bus=bus,service_chain=chain)

app = Flask(__name__)

@app.route("/test_addr0")
def test_addr0():
    return jsonify({"answer":1})

@app.route("/test_addr1")
def test_addr1():
    data=request.json   
    print(data)
    return jsonify({"answer":2})

@app.route("/")
def active():
    compute_handler.register_func()
    service_map.set_migration_service(us)

    return "ok"


if __name__ == '__main__':
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
