from flask import Blueprint
main = Blueprint('main', __name__)


@main.route('/')
def hello_world():
    return 'Hello World!'


@main.route('/handelMigration', methods=['POST']):

