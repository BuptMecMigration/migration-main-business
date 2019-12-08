from flask import Flask
import routes

app = Flask(__name__)


if __name__ == '__main__':
    routes.init_app(app)
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
