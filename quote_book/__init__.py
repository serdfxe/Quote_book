from flask import Flask
from quote_book.views.admin import admin
from quote_book.views.main import main
import secrets

def create_app():
    app = Flask(__name__)
    app.debug = 0
    app.secret_key = bytes(secrets.token_urlsafe(), 'utf-8')

    app.register_blueprint(main)

    return app
