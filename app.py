import threading

from flask import Flask
import routes
from common.code import MIGRATION_SERVICE_LISTEN_IP, MIGRATION_SERVICE_LISTEN_PORT
from migration.migration_handler import TCPHandler, ThreadedTCPServer

app = Flask(__name__)


if __name__ == '__main__':
<<<<<<< HEAD
    migration_start_receiver()
=======

    # 注册flask路由
>>>>>>> dev
    routes.init_app(app)
    print(app.url_map)

    # 多线程开启tcp server和flask功能
    workers = []
    workers.append(threading.Thread(target=app.run(host="0.0.0.0", port=5000, debug=True)))
    server = ThreadedTCPServer((MIGRATION_SERVICE_LISTEN_IP, MIGRATION_SERVICE_LISTEN_PORT), TCPHandler)
    workers.append(server.serve_forever())
    # workers.append(threading.Thread(target=simple_server()))

    for w in workers:
        w.start()
    # for w in workers:
    #     w.join()

    # 多进程开启server服务
    # workers.append(Process(target=app.run(host="0.0.0.0", port=5000, debug=True), daemon=True))
    # server = ThreadedTCPServer(('0.0.0.0', 9900), TCPHandler)
    # workers.append(Process(target=server.serve_forever(), daemon=True))
    # # workers.append(Process(target=app.run(host="0.0.0.0", port=5000, debug=True)))
    # for w in workers:
    #     w.start()
    # for w in workers:
    #     w.join()
