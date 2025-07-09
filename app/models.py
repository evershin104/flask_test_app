from datetime import datetime

from . import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (  # Fast serach for queries like `sentiment=positive, sort by created_at desc`
        db.Index(
            "idx_review_sentiment_created_desc", "sentiment", db.text("created_at DESC")
        ),
    )
