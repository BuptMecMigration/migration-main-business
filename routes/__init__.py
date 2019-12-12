from flask import Flask
# from . import main
from . import testInterface
from . import userInterface

# register the main_app
def init_app(app:Flask):
    # app.register_blueprint(main.main, url_prefix='/main')
    app.register_blueprint(userInterface.user_interface, url_prefix='/ui')
    app.register_blueprint(testInterface.test_interface, url_prefix='/test')
