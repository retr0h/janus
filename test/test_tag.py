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

from janus import node
from janus import tag


def test_all(create_node):
    result = tag.all_()
    assert 1 == len(result)
    assert isinstance(result, list)
    assert 'test-tag' == result[0]


def test_all_distinct(delete_all_nodes):
    node.create('test-node1', 'test-tag1')
    node.create('test-node2', 'test-tag1')
    node.create('test-node3', 'test-tag2')
    node.create('test-node4', 'test-tag3')

    result = tag.all_()
    assert 3 == len(result)


def test_find_all_by_tag(delete_all_nodes):
    node.create('test-node1', 'test-tag1')
    node.create('test-node2', 'test-tag1')
    node.create('test-node3', 'test-tag2')
    node.create('test-node4', 'test-tag3')

    result = tag.find_all_by_tag('test-tag1')
    assert 2 == len(result)
    assert isinstance(result, list)
    assert 'test-node1' in result[0].name
    assert 'test-node2' == result[1].name
