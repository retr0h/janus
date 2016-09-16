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

import contextlib

import sqlalchemy

from janus import conf

memo = {}


@contextlib.contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    """
    s = get_session()
    session = s()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        pass
        # closed on each request by flask
        # session.close()


@contextlib.contextmanager
def temp_scope():
    """
    Simple context manager that provides a temporary Session object to the
    nested block.
    """
    s = get_session()
    session = s()
    try:
        yield session
    except:
        raise
    finally:
        session.close()


def get_engine():
    """
    Create and return the sqlalchemy engine.  The result is memoized.

    :return: sqlalchemy.engine.base.Engine
    """
    engine = memo.get('engine')
    if engine:
        return engine
    else:
        engine = sqlalchemy.create_engine(conf.db_url())
        memo['engine'] = engine

        return engine


def get_session():
    """
    Create and return the sqlalchemy scoped session.  The result is memoized.

    :return: sqlalchemy.orm.scoping.scoped_session
    """
    session = memo.get('session')
    if session:
        return session
    else:
        engine = get_engine()
        session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
        session = sqlalchemy.orm.scoped_session(session_factory)
        memo['session'] = session

        return session
