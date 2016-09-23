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


def test_get(create_nodes, client):
    response = client.get('/node/test-node')
    assert 200 == response.status_code

    d = response.json.get('node')
    assert 'test-node' == d.get('name')
    assert 'test-tag' == d.get('tag')
    assert d.get('port')
    assert d.get('updated_at')
    assert d.get('created_at')


def test_get_not_found(create_nodes, client):
    response = client.get('/node/test-invalid')
    assert 404 == response.status_code
    assert '"Not Found"\n' == response.data


def test_delete(create_nodes, client):
    response = client.delete('/node/test-node')
    assert 204 == response.status_code
    assert '' == response.data


def test_delete_when_deleted(create_nodes, client):
    client.delete('/node/test-node')

    response = client.delete('/node/test-node')
    assert 404 == response.status_code
    assert '"Not Found"\n' == response.data
