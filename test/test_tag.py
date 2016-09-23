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

import pytest

from janus import tag


@pytest.mark.parametrize('create_nodes', [5], indirect=['create_nodes'])
def test_all(create_nodes):
    result = tag.all_()
    assert 5 == len(result)
    assert isinstance(result, list)
    assert 'test-tag0' == result[0]


@pytest.mark.parametrize('create_nodes', [5], indirect=['create_nodes'])
def test_all_distinct(create_nodes):
    result = tag.all_()
    assert 5 == len(result)


@pytest.mark.parametrize('create_nodes', [5], indirect=['create_nodes'])
def test_find_all_by_tag(create_nodes):
    pytest.helpers.create_node('test-node5', 'test-tag0')

    result = tag.find_all_by_tag('test-tag0')
    assert 2 == len(result)
    assert isinstance(result, list)
    assert 'test-node0' in result[0].name
    assert 'test-node5' == result[1].name
