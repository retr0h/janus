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


def test_get_port(create_nodes):
    assert 40000 == node.get_port('test-node')
    assert 40001 == node.get_port('test-new-host')


def test_get_next_port(delete_all_nodes):
    assert 40000 == node.get_next_port()

    pytest.helpers.create_node('test-node1', 'test-tag', 40000)
    pytest.helpers.create_node('test-node2', 'test-tag', 40001)

    assert 40002 == node.get_next_port()


@pytest.mark.parametrize('create_nodes', [5], indirect=['create_nodes'])
def test_get_next_port_backfill(create_nodes):
    pytest.helpers.delete_node('test-node3')
    pytest.helpers.delete_node('test-node4')

    assert 40003 == node.get_next_port()
    assert 40004 == node.get_next_port()
    assert 40005 == node.get_next_port()


def test_node_serialize(create_nodes):
    result = node.find_by_name('test-node').serialize
    assert 'test-node' == result.get('name')
    assert 'test-tag' == result.get('tag')
    assert isinstance(result.get('port'), long)
    assert isinstance(result.get('updated_at'), datetime.datetime)
    assert isinstance(result.get('created_at'), datetime.datetime)


@pytest.mark.parametrize('create_nodes', [5], indirect=['create_nodes'])
def test_all(create_nodes):
    result = node.all_()
    assert 5 == len(result)
    assert isinstance(result, list)


def test_all_filters_by_soft_deleted(create_nodes):
    pytest.helpers.delete_node('test-node')

    assert 0 == len(node.all_())


@pytest.mark.parametrize('create_nodes', [10], indirect=['create_nodes'])
def test_all_with_pagination(create_nodes):
    assert 5 == len(node.all_(5))
    assert 5 == len(node.all_(5, 1))
    assert 'test-node0' == node.all_(5)[0].name
    assert 'test-node5' == node.all_(5, 1)[0].name


def test_create(create_nodes):
    result = node.find_by_name('test-node')
    assert 'test-node' == result.name
    assert 'test-tag' == result.tag
    assert 40000 == result.port
    assert isinstance(result.updated_at, datetime.datetime)
    assert isinstance(result.created_at, datetime.datetime)


def test_delete(create_nodes):
    n = node.find_by_name('test-node')
    result = node.delete(n)
    assert result

    result = node.find_by_name('foo-hostname')
    assert not result


def test_delete_soft(create_nodes):
    pytest.helpers.delete_node('test-node')

    result = node.find_by_name('test-node', soft=True)
    assert isinstance(result.deleted_at, datetime.datetime)


@pytest.mark.parametrize('create_nodes', [2], indirect=['create_nodes'])
def test_find_deleted(create_nodes):
    pytest.helpers.delete_node('test-node0')
    pytest.helpers.delete_node('test-node1')

    result = node.find_deleted()
    assert 2 == len(result)
    assert isinstance(result, list)


def test_delete_returns_false():
    result = node.delete(None)
    assert not result


def test_delete_by_name(create_nodes):
    result = node.delete_by_name('test-node')
    assert result

    result = node.find_by_name('test-node')
    assert not result


@pytest.mark.parametrize('create_nodes', [2], indirect=['create_nodes'])
def test_delete_all(create_nodes):
    result = node.delete_all()
    assert 2 == result

    result = node.all_()
    assert 0 == len(result)


def test_name_unique_constraint(delete_all_nodes):
    assert pytest.helpers.create_node('test-node1', 'test-tag')
    assert not pytest.helpers.create_node('test-node1', 'test-tag')


def test_port_unique_constraint(delete_all_nodes):
    assert pytest.helpers.create_node('test-node1', 'test-tag', 40000)
    assert not pytest.helpers.create_node('test-node2', 'test-tag', 40000)


def test_port_min_range(delete_all_nodes):
    with pytest.raises(AssertionError) as e:
        pytest.helpers.create_node('test-node1', 'test-tag', 1024)
    assert "The port '1024' must be between 40000 and 50000!" in e.value
    pytest.helpers.create_node('test-node1', 'test-tag', 40000)


def test_port_max_range(delete_all_nodes):
    assert pytest.helpers.create_node('test-node1', 'test-tag', 50000)
    with pytest.raises(AssertionError) as e:
        pytest.helpers.create_node('test-node1', 'test-tag', 50001)
    assert "The port '50001' must be between 40000 and 50000!" in e.value
