from flask import Flask
from flask_httpauth import HTTPTokenAuth
from app.database import init_db
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')

def create_app():
    app = Flask(__name__)
    init_db()
    with app.app_context():
        from app.routes import api_keys, sitemap, logs
        app.register_blueprint(api_keys.bp)
        app.register_blueprint(sitemap.bp)
        app.register_blueprint(logs.bp)
    return app
