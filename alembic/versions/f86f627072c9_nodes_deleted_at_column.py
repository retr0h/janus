"""nodes deleted_at column

Revision ID: f86f627072c9
Revises: 5c0c27754e76
Create Date: 2016-09-20 15:19:45.923054

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f86f627072c9'
down_revision = '5c0c27754e76'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('nodes', sa.Column('deleted_at', sa.DateTime, nullable=True))


def downgrade():
    op.drop_column('nodes', 'deleted_at')
