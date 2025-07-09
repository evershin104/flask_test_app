from flask import Blueprint

from app.api import review_api

bp = Blueprint("main", __name__)


def register_api(app):
    app.register_blueprint(review_api.bp, url_prefix="/api/v1/app/reviews")
