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

blueprint = flask.Blueprint('node_blueprint', __name__)
api = flask_restful.Api(blueprint)
parser = flask_restful.reqparse.RequestParser()


class Node(flask_restful.Resource):
    def get(self, node_id):
        """
        ::

          /node/:node_id GET

        Response code: 200
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
        n = node.find_by_name(node_id)
        if n:
            return flask.jsonify(node=n.serialize)
        return 'Not Found', '404'

    def delete(self, node_id):
        """
        ::

          /node/:node_id DELETE

        Response code: 204
        Response data:

        .. code-block:: javascript

          No Content
        """
        n = node.find_by_name(node_id)

        if node.delete(n):
            return 'No Content', 204
        return 'Not Found', '404'

    def put(self, node_id):
        """
        """
        return 'put', 201


api.add_resource(Node, '/node/<node_id>')
