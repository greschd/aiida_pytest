#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os
import io
try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap
import json

import yaml
import temporary
import aiida
import django
import pytest

from ._input_mock import InputMock
from ._contextmanagers import redirect_stdin, redirect_stdout

@pytest.fixture(scope='session')
def reset_config_after_run():
    config_file = os.path.join(
        os.path.expanduser(aiida.common.setup.AIIDA_CONFIG_FOLDER),
        'config.json'
    )
    with open(config_file, 'r') as f:
        config_old = json.load(f)
    yield
    with open(config_file, 'w') as f:
        json.dump(config_old, f)

@pytest.fixture(scope='session')
def configure_from_file(configure):
    def inner(config_file):
        with open(config_file, 'r') as f:
            config = yaml.load(f)
        configure(config)
    return inner

@pytest.fixture(scope='session')
def configure(reset_config_after_run, flush_db_after_run):
    with temporary.temp_dir() as td:
        def inner(config):
            with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
                run_setup(repo_default=str(td), **config['setup'])
        yield inner

@pytest.fixture(scope='session')
def flush_db_after_run():
    yield
    from django.db import connections
    from django.core.management import call_command

    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        for db in connections:
            call_command('flush', verbosity=0, interactive=False, database=db)
        for conn in connections.all():
            conn.close()

def run_setup(repo_default, **kwargs):
    defaults = {
        'backend': 'django',
        'email': 'aiida@localhost',
        'first_name': 'Test',
        'last_name': 'User',
        'institution': 'Test Lab',
        'non_interactive': True,
        'only_config': False,
        'db_host': 'localhost',
        'db_port': '5432',
        'repo': repo_default
    }
    from aiida.cmdline.verdilib import setup
    setup(**ChainMap(kwargs, defaults))
