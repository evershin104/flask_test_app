import re
from datetime import datetime

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from ..models import Review, db
from ..schema import ReviewSchema

bp = Blueprint(
    "review_api", "review_api", url_prefix="/api/v1/reviews", description="Reviews API"
)

POSITIVE_WORDS = ["хорош", "люблю"]
NEGATIVE_WORDS = ["плохо", "ненавиж"]

# Скомпиленные паттерны поинтереснее чем каждое слово искать в строке, даже через any(...)
positive_pattern = re.compile(
    r"\b(?:" + "|".join(POSITIVE_WORDS) + r")\w*", re.IGNORECASE
)
negative_pattern = re.compile(
    r"\b(?:" + "|".join(NEGATIVE_WORDS) + r")\w*", re.IGNORECASE
)


@bp.route("/")
class ReviewList(MethodView):
    """View class"""

    PAGE_SIZE: int = 10
    # Pagination

    @staticmethod
    def __detect_sentiment(text: str) -> str:
        """Defines sentiment
        Args:
            text: input text
        Returns:
            Any["positive", "negative", "neutral"]
        """
        if positive_pattern.search(text):
            return "positive"
        if negative_pattern.search(text):
            return "negative"
        return "neutral"

    @bp.response(200, ReviewSchema(many=True))
    def get(self, *args, **kwargs):
        """Get requests handler
        Returns:
            Paginated page with reviews. Reviews can be filtered
            by sentiment=<value> and always sorted by created_at
        """
        sentiment_filter = request.args.get("sentiment")
        page = request.args.get("page", 1, type=int)

        query = Review.query.order_by(Review.created_at.desc())

        if sentiment_filter in {"positive", "negative", "neutral"}:
            query = query.filter(Review.sentiment == sentiment_filter)

        paginated = query.paginate(page=page, per_page=self.PAGE_SIZE, error_out=False)
        return paginated.items

    @bp.arguments(ReviewSchema(only=("text",)))
    @bp.response(201, ReviewSchema)
    def post(self, _request: dict, *args, **kwargs):
        text = _request["text"]
        sentiment = self.__detect_sentiment(text)

        review = Review(text=text, sentiment=sentiment, created_at=datetime.utcnow())
        db.session.add(review)
        db.session.commit()

        return review
