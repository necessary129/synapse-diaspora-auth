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

Email Authentication
~~~~~~~~~~~~~~~~~~~~

While this module helps in authenticating with diaspora, we need to set up mxisd_ for supporting
authentication through email.

Installation
^^^^^^^^^^^^

Follow the instructions `here <https://github.com/kamax-io/mxisd/blob/master/docs/getting-started.md#install>`_

Configuration & Setup
^^^^^^^^^^^^^^^^^^^^^

Follow `this <https://github.com/kamax-io/mxisd/blob/master/docs/getting-started.md#configure>`_.

Basically, if you used the debian package, you just need to set up the ``matrix.domain`` first.

And then, add these lines to ``mxisd.yaml``:

.. code:: yaml

    sql:
      enabled: true
      type: mysql
      connection: "//<HOST>/<DATABASE>?user=<USERNAME>&password=<PASSWORD>"
      identity:
        type: 'uid'
        query: "select (case when ?='email' then username else null end) as uid from users where email=?"

Where ``<HOST>``, ``<DATABASE>``,``<USERNAME>`` and ``<PASSWORD>`` are your database host, diaspora database, user and password you created when you set up database for synapse-diaspora-auth

Now follow the steps `here <https://github.com/kamax-io/mxisd/blob/master/docs/features/authentication.md#advanced>`_. ie, forward the ``/_matrix/client/r0/login`` endpoint to mxisd and add

.. code:: yaml

    dns.overwrite.homeserver.client:
      - name: '<DOMAIN>'
        value: 'http://localhost:8008'

where ``<DOMAIN>`` is your matrix server name.

An Apache2 reverse proxy example is already given `here <https://github.com/kamax-io/mxisd/blob/master/docs/features/authentication.md#apache2>`_. An example nginx configuration would be this:

.. code::

    location /_matrix/client/r0/login {
        proxy_pass http://localhost:8090/_matrix/client/r0/login;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

Make sure to put this above other matrix reverse proxy directives. And Congrats! You now have a competely integrated synapse - diaspora setup! :D

.. _mxisd: https://github.com/kamax-io/mxisd