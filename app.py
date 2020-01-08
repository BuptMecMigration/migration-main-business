import threading

from flask import Flask
import routes
from common.code import MIGRATION_SERVICE_LISTEN_IP, MIGRATION_SERVICE_LISTEN_PORT, SERVER_PORT
from migration.migration_handler import TCPHandler, ThreadedTCPServer, add_server_address
from routes.main.handler import compute_handler
app = Flask(__name__)


if __name__ == '__main__':

    def flask_run():
        # app.run(host="0.0.0.0", port=5000, debug=True)
        add_server_address(MIGRATION_SERVICE_LISTEN_PORT)
        app.run(host="0.0.0.0", port=SERVER_PORT)

    def migration_server_run():
        print("开始监听IP位置: {} 端口号: {}".format(MIGRATION_SERVICE_LISTEN_IP, MIGRATION_SERVICE_LISTEN_PORT))
        ThreadedTCPServer((MIGRATION_SERVICE_LISTEN_IP, MIGRATION_SERVICE_LISTEN_PORT), TCPHandler).serve_forever()

    # 注册flask路由
    routes.init_app(app)
    print(app.url_map)

    # 多线程开启tcp server和flask功能
    workers = [ ]
    workers.append(threading.Thread(target=flask_run, daemon=True))
    workers.append(threading.Thread(target=migration_server_run, daemon=True))
    # workers.append(threading.Thread(target=simple_server()))


    # register_func of compute_handler
    compute_handler.register_func()
    
    for w in workers:
        w.start()
    for w in workers:
        w.join()
