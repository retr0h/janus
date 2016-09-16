Testing
=======

.. code-block:: bash

  $ make
  $ source venv/bin/activate
  $ docker pull mysql
  $ docker run -p 3306:3306 \
    -e MYSQL_USER=janus \
    -e MYSQL_PASSWORD=janus-pass \
    -e MYSQL_DATABASE=janus \
    -e MYSQL_ROOT_PASSWORD=root-pass \
    -d mysql:latest
  $ mysql -uroot --protocol=TCP -p
  $ env $(cat .env | xargs) alembic version
  $ env $(cat .env | xargs) python janus/app/app.py
  $ env $(cat .env | xargs) py.test test/app/test_nodes.py

Unit
----

.. code-block:: bash

	$ tox
