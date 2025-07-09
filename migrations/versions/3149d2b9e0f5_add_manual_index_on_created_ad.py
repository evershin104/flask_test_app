"""Add manual index on created_ad

Revision ID: 3149d2b9e0f5
Revises: 8b892e7403cd
Create Date: 2025-07-09 22:41:36.156802

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3149d2b9e0f5"
down_revision = "8b892e7403cd"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("idx_review_created", "reviews", ["created_at"], unique=False)


def downgrade():
    op.drop_index("idx_review_created", table_name="reviews")
