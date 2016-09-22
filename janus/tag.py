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
"""
Broke this out into a module, since we will likely move to n to 1 relationship.
"""

from janus import client
from janus import models
from janus import node


def all_():
    """
    Finds and returns a list of all non-deleted tags.

    :return: list
    """
    with client.session_scope() as session:
        tags = session.query(models.Node.tag).distinct().all()

        return list(sum(tags, ()))


def find_all_by_tag(tag):
    """
    Find the given tag, and return a list of all node objects.

    :param tag: A string containing the tag to find.
    :return: list
    """
    with client.temp_scope() as session:
        n = models.Node
        return (session.query(n).filter(n.tag == tag)
                .filter(n.deleted_at.is_(None)).order_by(n.tag).all())
