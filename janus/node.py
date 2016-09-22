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

import sqlalchemy.exc

from janus import client
from janus import conf
from janus import models


def get_port(name):
    """
    Find a hosts assigned port, otherwise assign a port and return it.

    :param name: A string containing the name to find.
    :return: int
    """
    node = find_by_name(name)
    if node:
        return node.port
    return get_next_port()


def get_next_port():
    """
    Find and return the next available port.

    :return: int
    """
    deleted = find_deleted()
    if deleted:
        n = deleted.pop(0)
        port = n.port
        with client.session_scope() as session:
            n.deleted_at = None
            session.add(n)
        return port
    with client.session_scope() as session:
        n = models.Node
        return session.query(n).count() + conf.port_start()


def all_():
    """
    Finds and returns a list of all non-deleted nodes.

    :return: list
    """
    with client.session_scope() as session:
        n = models.Node
        return (session.query(n).filter(n.deleted_at.is_(None)).all())


def create(name, tag, port=None):
    """
    Creates a node with the given name/port, and returns the object.

    :param name: A string containing the name to create.
    :param tag: A string containing name to tag the node with.
    :param port: An optional int containing the port to create.
    :return: :class:`.Node`
    """
    if port is None:
        port = get_port(name)
    try:
        n = models.Node(name=name, tag=tag, port=port)
        with client.session_scope() as session:
            session.add(n)

            return n
    except sqlalchemy.exc.IntegrityError:
        return


def delete(obj, soft=True):
    """
    Deletes the given object, and returns a bool.

    :param obj: The :class:`.Node` object to delete.
    :return: bool
    """
    if obj:
        if soft:
            return _soft_delete(obj)
        else:
            with client.session_scope() as session:
                session.delete(obj)

                return True


def _soft_delete(obj):
    with client.session_scope() as session:
        obj.deleted_at = datetime.datetime.utcnow()
        session.add(obj)

        return True


def delete_by_name(name):
    """
    Delete the given name, and return bool.

    :param name: A string containing the name to delete.
    :return: bool
    """
    node = find_by_name(name)
    if node:
        return delete(node)


def delete_all():
    """"
    Delete all rows, and return the count of rows matched as returned by
    the database's "row count" feature.

    :return: int
    """
    with client.session_scope() as session:
        return session.query(models.Node).delete()


def find_by_name(name, soft=False):
    """
    Find the given name, and returns the object.

    :param name: A string containing the name to find.
    :return: :class:`.Node`
    """
    with client.temp_scope() as session:
        n = models.Node
        q = session.query(n).filter(n.name == name)
        if not soft:
            q = q.filter(n.deleted_at.is_(None))

        return q.first()


def find_deleted():
    """
    Finds and returns a list of all deleted nodes.

    :return: list
    """
    with client.temp_scope() as session:
        n = models.Node
        return (session.query(n).filter(n.deleted_at.isnot(None))
                .order_by(n.port).all())
