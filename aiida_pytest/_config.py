#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os
import io
import json

import yaml
import temporary
import aiida
import django
import pytest

from ._input_helper import InputHelper
from ._contextmanagers import redirect_stdin, redirect_stdout

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
            from ._setup import run_setup
            with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
                run_setup(repo_default=str(td), **config['setup'])

            from ._computer import setup_computer
            computers = config.get('computers', [])
            for computer_kwargs in computers:
                setup_computer(**computer_kwargs)
            from ._code import setup_code
            codes = config.get('codes', [])
            for code_kwargs in codes:
                setup_code(**code_kwargs)
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
