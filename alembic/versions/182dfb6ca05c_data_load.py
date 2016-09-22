"""data load

Revision ID: 182dfb6ca05c
Revises: 5a56b3ef19cf
Create Date: 2016-09-22 18:31:30.011417

"""
import datetime
import random
import string

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '182dfb6ca05c'
down_revision = '5a56b3ef19cf'
branch_labels = None
depends_on = None
port_start = 40000
port_end = 50000


def random_string(l=12):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(l))


def random_tag(n):
    if n % 10 == 0 or n % 10 == 10:
        n = 2
    else:
        n = 1
    return 'test-tag{}'.format(n)


def create_time():
    return datetime.datetime.utcnow()


def build_data():
    return [{'id': n,
             'name': random_string(),
             'port': n,
             'tag': random_tag(n),
             'created_at': create_time(),
             'upgraded_at': create_time()}
            for n in range(port_start, port_end)]


def upgrade():
    nodes_table = sa.Table('nodes', sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('port', sa.Integer, nullable=False),
        sa.Column('tag', sa.String(64), nullable=True, index=True),
        sa.UniqueConstraint('name', name='name_uix'),
        sa.UniqueConstraint('port', name='port_uix'))

    op.bulk_insert(nodes_table, build_data())


def downgrade():
    pass
