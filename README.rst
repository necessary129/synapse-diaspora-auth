Synapse-diaspora-auth
=====================

A diaspora authenticator for matrix synapse.

Installation
------------

This package is easy to install from pypi:

Just run this command to install:

.. code:: bash

    pip install synapse-diaspora-auth

Alternatively, to install from git:

.. code:: bash

    pip install git+https://git.fosscommunity.in/necessary129/synapse-diaspora-auth.git

Configuration
-------------

In your ``homeserver.yaml`` file, the ``password_providers`` directive
should look like this:

.. code:: yaml

    password_providers:
      - module: "diaspora_auth_provider.DiasporaAuthProvider"
        config:
          pepper: <pepper>
          database:
            engine: <db engine>
            name: "<database>"
            username: <db_user>
            password: <db_password>
            host: "127.0.0.1"
            port: <port>

You should get ``pepper`` from ``<DIASPORA_HOME>/database.yaml`` or from
``<DIASPORA_HOME>/initializers/devise.rb`` as ``config.pepper``.

the engine should either be ``mysql`` or ``postgres``

The port is usually ``5432`` for PostgreSQL and ``3306`` for MariaDB/MySQL

Database
~~~~~~~~

synapse-diaspora-auth currently supports MySQL and PostgreSQL as the database engines.

PostgreSQL
^^^^^^^^^^

It is recommended to create a seperate user for synapse in the postgres
database, with read-only access to ``<database>``.

To do that, first login to postgres as the root user:

.. code:: bash

    sudo -u postgres psql <database>

then, run these commands:

.. code:: sql

    CREATE user <db_user> WITH password '<db_password>';
    GRANT CONNECT ON DATABASE <database> TO <db_user>;
    GRANT SELECT ON users TO <db_user>;

MySQL
^^^^^

The commands are almost the same in MySQL:

login to MySQL as root:

.. code:: bash

    sudo mysql -u root

Then run these queries:

.. code:: sql

    CREATE user '<db_user>'@'localhost' WITH password '<db_password>';
    GRANT SELECT ON <database>.users TO '<db_user>'@'localhost';


And you will be good to go!