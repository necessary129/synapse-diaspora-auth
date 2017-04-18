Synapse-diaspora-auth
=====================

A diaspora authenticator for matrix synapse.

Installation
------------

This package is not submitted to pypi yet, so you would have to make do
with the repo.

Just run this command to install:

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
            name: "diaspora_production"
            username: <db_user>
            password: <db_password>
            host: "127.0.0.1"
            port: 5432

You should get ``pepper`` from ``<DIASPORA_HOME>/database.yaml`` or from
``<DIASPORA_HOME>/initializers/devise.rb`` as ``config.pepper``.

Database
~~~~~~~~

It is recommended to create a seperate user for synapse in the postgres
database, with read-only access to ``diaspora_production``.

To do that, first login to postgres as the root user:

.. code:: bash

    sudo -u postgres psql diaspora_production

then, run these commands:

.. code:: sql

    CREATE user <db_user> WITH password '<db_password>';
    GRANT CONNECT ON DATABASE diaspora_production TO <db_user>;
    GRANT SELECT ON users TO <db_user>;

And you will be good to go!