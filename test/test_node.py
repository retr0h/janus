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

import pytest

from janus import node


def test_get_port(delete_all_nodes):
    node.create('test-existing-host', 40000)

    assert 40000 == node.get_port('test-existing-host')
    assert 40001 == node.get_port('test-new-host')


def test_get_next_port(delete_all_nodes):
    assert 40000 == node.get_next_port()

    node.create('test-node1', 40000)
    node.create('test-node2', 40001)

    assert 40002 == node.get_next_port()


@pytest.mark.skip(reason="backfill fails, core needs reworked")
def test_get_next_port_backfill(delete_all_nodes):
    node.create('test-node1', 40001)
    node.create('test-node2', 40002)
    node.create('test-node3', 40003)
    node.create('test-node4', 40004)
    node.create('test-node5', 40005)
    node.create('test-node6', 40006)

    node.delete_by_name('test-node3')

    assert 40007 == node.get_next_port()


def test_node_serialize(create_node):
    result = node.find_by_name('test-node').serialize
    assert isinstance(result.get('port'), long)
    assert isinstance(result.get('updated_at'), datetime.datetime)
    assert isinstance(result.get('created_at'), datetime.datetime)


def test_all(create_node):
    result = node.all()
    assert 1 == len(result)
    assert isinstance(result, list)


def test_create(delete_all_nodes):
    node.create('test-node')
    node.create('test-new-node')

    result = node.find_by_name('test-node')
    assert 40000 == result.port

    result = node.find_by_name('test-new-node')
    assert 'test-new-node' == result.name
    assert 40001 == result.port
    assert isinstance(result.updated_at, datetime.datetime)
    assert isinstance(result.created_at, datetime.datetime)


def test_delete(create_node):
    n = node.find_by_name('test-node')
    result = node.delete(n)
    assert result

    result = node.find_by_name('foo-hostname')
    assert not result


def test_delete_returns_false():
    result = node.delete(None)
    assert not result


def test_delete_by_name(create_node):
    result = node.delete_by_name('test-node')
    assert result

    result = node.find_by_name('test-node')
    assert not result


def test_delete_all():
    node.create('test-node1')
    node.create('test-node2')

    result = node.delete_all()
    assert 2 == result

    result = node.all()
    assert 0 == len(result)


def test_name_unique_constraint(delete_all_nodes):
    assert node.create('test-node1')
    assert not node.create('test-node1')


def test_port_unique_constraint(delete_all_nodes):
    assert node.create('test-node1', 40000)
    assert not node.create('test-node2', 40000)


def test_port_min_range(delete_all_nodes):
    with pytest.raises(AssertionError) as e:
        node.create('test-node1', 1024)
    assert "The port '1024' must be between 40000 and 50000!" in e.value
    assert node.create('test-node1', 40000)


def test_port_max_range(delete_all_nodes):
    assert node.create('test-node1', 50000)
    with pytest.raises(AssertionError) as e:
        node.create('test-node1', 50001)
    assert "The port '50001' must be between 40000 and 50000!" in e.value
