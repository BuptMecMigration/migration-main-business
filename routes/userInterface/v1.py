from flask import Blueprint
user_interface = Blueprint('user_interface', __name__)

@user_interface.route('/')
def hello_world():
    return 'Hello World!'