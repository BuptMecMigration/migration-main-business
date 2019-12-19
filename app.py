from flask import Flask
import routes
from migration.migration_handler import migration_start_receiver

app = Flask(__name__)


if __name__ == '__main__':
    # 启动迁移部分监听TCPServer
    workers = []
    work_list = migration_start_receiver(workers)
    [w.join() for w in work_list]
    routes.init_app(app)
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
