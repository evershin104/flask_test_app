from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .api.review_api import bp as review_bp
    from .models import Review

    api = Api(app)
    api.register_blueprint(review_bp)

    return app
