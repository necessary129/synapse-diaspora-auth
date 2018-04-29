#!/usr/bin/env python

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

from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

def read(file_path):
    path = os.path.join(here, file_path)
    with open(path) as f:
        return f.read()

def exec_file(path_segments, name):
    """Extract a constant from a python file by looking for a line defining
    the constant and executing it."""
    result = {}
    code = read(path_segments)
    lines = [line for line in code.split('\n') if line.startswith(name)]
    exec("\n".join(lines), result)
    return result[name]

setup(
    name="synapse-diaspora-auth",
    author="Shamil K",
    author_email="noteness@riseup.net",
    license="GPLv3",
    keywords="matrix synapse diaspora authentication",

    version=exec_file("diaspora_auth_provider.py", "__VERSION__"),
    py_modules=["diaspora_auth_provider"],
    description="A Diaspora* auth provider for Synapse",
    install_requires=[
        "Twisted>=15.1.0",
        "psycopg2",
        "bcrypt",
        "pymysql"
    ],
    long_description=read("README.rst"),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Chat'
    ],
)


