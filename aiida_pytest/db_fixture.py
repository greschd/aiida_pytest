#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from temporary import temp_dir

import aiida
import pytest
from pgtest.pgtest import PGTest

@pytest.fixture(scope='session')
def aiidadb():
    with PGTest() as pgt, temp_dir() as td:
        monkeypatch_config(pg_port=pgt.port, repo_path=str(td))
        aiida.load_dbenv()
        # from aiida.cmdline.verdilib import setup
        # Setup().run()
        # from aiida.cmdline.commands.code import Code
        # Code().code_setup()
        yield

def monkeypatch_config(pg_port, repo_path):
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
    aiida.common.AIIDA_CONFIG_FOLDER = os.path.abspath(repo_path)
