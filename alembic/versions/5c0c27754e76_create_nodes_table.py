"""create nodes table

Revision ID: 5c0c27754e76
Revises: 
Create Date: 2016-09-16 13:23:28.418629

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5c0c27754e76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'nodes',
        sa.Column(
            'id', sa.Integer, primary_key=True),
        sa.Column(
            'created_at', sa.DateTime, nullable=False),
        sa.Column(
            'updated_at', sa.DateTime, nullable=False),
        sa.Column(
            'name', sa.String(50), nullable=False),
        sa.Column(
            'port', sa.Integer, nullable=False),
        sa.UniqueConstraint(
            'name', name='name_uix'),
        sa.UniqueConstraint(
            'port', name='port_uix'))


def downgrade():
    op.drop_table('nodes')
