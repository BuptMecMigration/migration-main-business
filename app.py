from flask import Flask
import routes
from migration.migration_handler import migration_start_receiver

app = Flask(__name__)


if __name__ == '__main__':
    migration_start_receiver()
    routes.init_app(app)
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
