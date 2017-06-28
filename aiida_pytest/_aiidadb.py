#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import io
import os
from temporary import temp_dir

import aiida
import pytest
from pgtest.pgtest import PGTest

from ._input_mock import InputMock
from ._contextmanagers import redirect_stdin, redirect_stdout

__all__ = ['aiidadb']

@pytest.fixture(scope='session')
def aiidadb():
    with PGTest() as pgt, temp_dir() as td:
        monkeypatch_config(pg_port=pgt.port, repo_path=str(td))
        run_setup()
        # avoid double load_dbenv
        aiida.load_dbenv = lambda: None
        setup_localhost(str(td))
        from aiida.cmdline.verdilib import exec_from_cmdline
        exec_from_cmdline(['verdi', 'computer', 'list'])
        yield

def monkeypatch_config(pg_port, repo_path):
    aiida.common.setup.AIIDA_CONFIG_FOLDER = os.path.abspath(repo_path)
    def get_test_config():
        return {
            "default_profiles": {"daemon": "default", "verdi": "default"},
            "profiles": {
                "default": {
                    "AIIDADB_ENGINE": "postgresql_psycopg2", "AIIDADB_PASS": "", "AIIDADB_NAME": "postgres", "AIIDADB_HOST": "localhost", "AIIDADB_BACKEND": "django", "default_user_email": "aiida@localhost", "AIIDADB_USER": "postgres", "AIIDADB_PORT": pg_port, "AIIDADB_REPOSITORY_URI": 'file://' + os.path.join(repo_path, '.aiida', 'repository')
                }
            }
        }
    aiida.common.setup.get_config = get_test_config

def run_setup():
    from aiida.cmdline.verdilib import Setup
    # Python 3: contextlib.redirect_stdout
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        with redirect_stdin(io.StringIO('N\n')):
            Setup().run()

def setup_localhost(tmpfolder):
    from aiida.cmdline.commands.computer import Computer
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        run_path = os.path.join(tmpfolder, 'aiida_run')
        computer_setup_input = InputMock(input=[
            'localhost', 'localhost', 'Local Computer', 'True', 'local', 'direct',
            run_path, 'mpirun -np {tot_num_mpiprocs}' , '1', None, None
        ])
        with redirect_stdin(computer_setup_input):
            Computer().computer_setup()
            Computer().computer_configure('localhost')
