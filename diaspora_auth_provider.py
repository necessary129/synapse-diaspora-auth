"""
synapse-diaspora-auth: A diaspora authenticator for matrix synapse.
Copyright (C) 2017 Shamil K Muhammed.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from twisted.internet import defer, threads

import bcrypt

import logging

__VERSION__ = "0.0.4"

logger = logging.getLogger(__name__)


class DiasporaAuthProvider:
    __version__ = "0.0.4"

    def __init__(self, config, account_handler):
        self.account_handler = account_handler
        self.config = config
        if self.config.engine == "mysql":
            import pymysql
            self.module = pymysql
        elif self.config.engine == 'postgres':
            import psycopg2
            self.module = psycopg2
        self.connection = self.module.connect(
            database=self.config.db_name,
            user=self.config.db_username,
            password=self.config.db_password,
            host=self.config.db_host,
            port=self.config.db_port
        )

    @defer.inlineCallbacks
    def check_password(self, user_id, password):
        if not password:
            defer.returnValue(False)
        # user_id is @localpart:hs_bare. we only need the localpart.
        local_part = user_id.split(':', 1)[0][1:]
        logger.info("Checking if user {} exists.".format(local_part))
        try:
            with self.connection.cursor() as cursor:
                yield threads.deferToThread( # Don't think this is needed, but w/e
                    cursor.execute,
                    "SELECT username, encrypted_password FROM users WHERE username=%s",
                    (local_part,)
                )
                user = yield threads.deferToThread(
                    cursor.fetchone
                )
            # check if the user exists.
            if not user:
                logger.info("User {} does not exist. Rejecting auth request".format(local_part))
                defer.returnValue(False)
            logger.debug("User {} exists. Checking password".format(local_part))
            # user exists, check if the password is correct.
            encrypted_password = user[1]
            peppered_pass = "{}{}".format(password, self.config.pepper)
            if not (bcrypt.hashpw(peppered_pass.encode('utf8'), encrypted_password.encode('utf8'))
                        == encrypted_password.encode('utf8')):
                logger.info("Password given for {} is wrong. Rejecting auth request.".format(local_part))
                defer.returnValue(False)
            # Ok, user's password is correct. check if the user exists in the homeserver db.
            # and create it if doesn't exist.
            if (yield self.account_handler.check_user_exists(user_id)):
                logger.info("User {} does exist in synapse db. Authentication complete".format(local_part))
                defer.returnValue(True)
            # User not in synapse db. need to create it.
            logger.info("User {} does not exist in synapse db. creating it.".format(local_part))
            user_id, access_token = (
                yield self.account_handler.register(localpart=local_part)
            )
            logger.info(
                "Registration based on diaspora complete. UserID: {}.".format(user_id)
            )
            logger.info("Confirming authentication request.")
            defer.returnValue(True)
        except self.module.Error as e:
            logger.warning("Error during diaspora authentication: {}".format(e))
            defer.returnValue(False)

    @staticmethod
    def parse_config(config):
        class _Conf:
            pass
        Conf = _Conf()
        Conf.engine = config['database']['engine']
        Conf.db_name = "diaspora_production" if not config['database']['name'] else config['database']['name']
        Conf.db_host = config['database']['host']
        Conf.db_port = config['database']['port']
        Conf.db_username = config['database']['username']
        Conf.db_password = config['database']['password']
        Conf.pepper = config['pepper']
        return Conf

