from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "trocar-em-producao"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secretaria.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from . import models  # noqa: F401
    from .routes import register_routes

    with app.app_context():
        db.create_all()
        models.ensure_admin_user()

    register_routes(app)
    return app
