#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import io
import os
import sys
import contextlib
from temporary import temp_dir

import aiida
import pytest
from pgtest.pgtest import PGTest

@contextlib.contextmanager
def redirect_stdout(target):
    original = sys.stdout
    sys.stdout = target
    yield
    sys.stdout = original

@contextlib.contextmanager
def redirect_stdin(target):
    original = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = original

@pytest.fixture(scope='session')
def aiidadb():
    with PGTest() as pgt, temp_dir() as td:
        monkeypatch_config(pg_port=pgt.port, repo_path=str(td))
        aiida.load_dbenv()
        # avoid double load_dbenv
        aiida.load_dbenv = lambda: None
        run_setup()
        # setup_localhost(str(td))
        # from aiida.cmdline.verdilib import exec_from_cmdline
        # exec_from_cmdline(['verdi', 'computer', 'list'])
        # yield

def monkeypatch_config(pg_port, repo_path):
    aiida.common.AIIDA_CONFIG_FOLDER = os.path.abspath(repo_path)
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
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull), redirect_stdin(io.StringIO('N\n')):
        Setup().run()

def setup_localhost(tmpfolder):
    class ComputerSetupInput:
        """
        Class to mock the input for computer setup. This is needed because io.StringIO cannot create the EOFError needed to end the multiline inputs.
        """
        def __init__(self, run_path):
            self.input = [
                'localhost', 'localhost', 'Local Computer', 'True', 'local', 'direct',
                run_path, 'mpirun -np {tot_num_mpiprocs}' , '1', None, None
            ]

        def readline(self):
            try:
                res = self.input.pop(0)
                if res is None:
                    raise EOFError
                return res
            except IndexError:
                raise EOFError

    from aiida.cmdline.commands.computer import Computer
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull), redirect_stdin(ComputerSetupInput(os.path.join(tmpfolder, 'aiida_run'))):
        Computer().computer_setup()
        Computer().computer_configure('localhost')
