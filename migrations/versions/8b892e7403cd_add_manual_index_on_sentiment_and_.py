"""Add manual index on sentiment and created_at

Revision ID: 8b892e7403cd
Revises: 6c3dd67a6319
Create Date: 2025-07-09 22:22:06.187406

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8b892e7403cd"
down_revision = "6c3dd67a6319"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "idx_review_sentiment_created",
        "reviews",
        ["sentiment", "created_at"],
        unique=False,
    )


def downgrade():
    op.drop_index("idx_review_sentiment_created", table_name="reviews")
