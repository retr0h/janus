import flask

from janus import client
from janus.app import node
from janus.app import nodes
from janus.app import tag
from janus.app import tags


def before_request():
    s = client.get_session()
    flask.g.session = s()


def after_request(response):
    flask.g.session.close()

    return response


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object('envcfg.json.janus')
    app.before_request(before_request)
    app.after_request(after_request)

    app.register_blueprint(tags.blueprint)
    app.register_blueprint(tag.blueprint)
    app.register_blueprint(nodes.blueprint)
    app.register_blueprint(node.blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
