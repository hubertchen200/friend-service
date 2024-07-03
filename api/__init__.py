from flask import Flask

print('api init')
from api.routes.friend_routes import friend_bp


def create_app():
    app = Flask(__name__)
    print('create app')
    app.register_blueprint(friend_bp)
    return app
