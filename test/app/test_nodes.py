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


def test_get(client, create_node):
    response = client.get('/nodes')
    assert 200 == response.status_code
    assert 1 == len(response.json)

    assert {'nodes': ['test-node']} == response.json


def test_post(client, delete_all_nodes):
    data = {"name": "test-nodename"}
    response = client.post('/nodes', data=data)
    assert 201 == response.status_code

    nd = response.json.get('node')
    assert 'test-nodename' == nd.get('name')


def test_post_when_exists(client, delete_all_nodes):
    data = {"name": "test-nodename"}
    client.post('/nodes', data=data)

    response = client.post('/nodes', data=data)
    assert 409 == response.status_code
