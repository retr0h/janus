# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2016 Cisco Systems, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import datetime

import sqlalchemy
import sqlalchemy.ext.declarative

from janus import client
from janus import conf

Base = sqlalchemy.ext.declarative.declarative_base()
engine = client.get_engine()
metadata = sqlalchemy.MetaData(bind=engine)


class BaseMixin(object):
    @staticmethod
    def create_time(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.created_at = now
        instance.updated_at = now

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.updated_at = now

    @classmethod
    def register(cls):
        sqlalchemy.event.listen(cls, 'before_insert', cls.create_time)
        sqlalchemy.event.listen(cls, 'before_update', cls.update_time)


class Node(Base, BaseMixin):
    __table__ = sqlalchemy.Table('nodes', metadata, autoload=True)

    def __repr__(self):
        obj = ('(<Node: id={}, name={}, port={}, created_at={}, '
               'updated_at={}, deleted_at={}>)')

        return obj.format(self.id, self.name, self.port, self.created_at,
                          self.updated_at, self.deleted_at)

    @sqlalchemy.orm.validates('port')
    def validate_port(self, key, port):
        msg = "The port '{}' must be between {} and {}!".format(
            port, conf.port_start(), conf.port_end())

        assert port >= conf.port_start(), msg
        assert port <= conf.port_end(), msg

        return port

    @property
    def serialize(self):
        """ Return object data in easily serializeable format. """

        return {
            'id': self.id,
            'name': self.name,
            'port': self.port,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


Node.register()
