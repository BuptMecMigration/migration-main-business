from flask import Flask
from . import main
from . import userInterface

# register the main_app
def init_app(app:Flask):
    app.register_blueprint(main.main, url_prefix='/main')
    app.register_blueprint(userInterface.user_interface, url_prefix='/ui')