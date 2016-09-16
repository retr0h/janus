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

import flask
import flask_restful
import flask_restful.reqparse

from janus import node

blueprint = flask.Blueprint('nodes_blueprint', __name__)
api = flask_restful.Api(blueprint)
parser = flask_restful.reqparse.RequestParser()


class Nodes(flask_restful.Resource):
    def get(self):
        """
        ::

          /nodes GET

        Response code: 200
        Response data:

        .. code-block:: javascript

          {
            "nodes": [
              "node1",
              "node2",
              "node3"
            ]
          }
        """
        return flask.jsonify(nodes=[result.name for result in node.all()])

    def post(self):
        """
        ::

          /nodes POST

        Request data

        .. code-block:: javascript

          {
              "name": str
          }

        Response code: 201
        Response data:

        .. code-block:: javascript

          {
            "node": {
              "name": str,
              "port": int,
              "created_at": datetime,
              "updated_at": datetime
            }
          }

        """
        parser.add_argument('name')
        args = parser.parse_args()
        node_id = args.get('name')

        if node.find_by_name(node_id):
            return 'Conflict', 409

        n = node.create(node_id)
        if n:
            return flask.make_response(flask.jsonify(node=n.serialize), 201)


api.add_resource(Nodes, '/nodes')
