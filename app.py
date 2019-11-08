from flask import Flask
from  gevent.pywsgi import WSGIServer
from gevent import monkey


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 80), app)
    http_server.serve_forever()
