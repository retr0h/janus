"""nodes tag column

Revision ID: 5a56b3ef19cf
Revises: f86f627072c9
Create Date: 2016-09-22 14:56:44.029375

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5a56b3ef19cf'
down_revision = 'f86f627072c9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'nodes', sa.Column(
            'tag', sa.String(64), nullable=True, index=True))


def downgrade():
    op.drop_column('nodes', 'tag')
