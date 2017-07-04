#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os
import json
import shutil
from contextlib import contextmanager

import yaml
import temporary
from pgtest.pgtest import PGTest
import aiida
import django
import pytest

from ._input_helper import InputHelper
from .contextmanagers import redirect_stdin, redirect_stdout

@pytest.fixture(scope='session')
def configure():
    with open(os.path.abspath('config.yml'), 'r') as f:
        config = yaml.load(f)

    with temporary.temp_dir() as td, PGTest() as pgt:
        with reset_config_after_run():
            # flush_db()
            from ._setup import run_setup
            with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
                run_setup(
                    profile='test_profile',
                    db_user='postgres',
                    db_port=pgt.port,
                    db_name='postgres',
                    db_pass='',
                    repo=str(td)
                )

            from ._computer import setup_computer
            computers = config.get('computers', [])
            for computer_kwargs in computers:
                setup_computer(**computer_kwargs)

            from ._code import setup_code
            codes = config.get('codes', [])
            for code_kwargs in codes:
                setup_code(**code_kwargs)

            with handle_daemon():
                yield

@contextmanager
def reset_config_after_run():
    config_folder = os.path.expanduser(aiida.common.setup.AIIDA_CONFIG_FOLDER)
    config_save_folder = os.path.join(os.path.dirname(config_folder), '.aiida~')
    reset_config(config_folder, config_save_folder)
    shutil.copytree(config_folder, config_save_folder)
    yield
    reset_config(config_folder, config_save_folder)

def reset_config(config_folder, config_save_folder):
    if os.path.isdir(config_save_folder):
        shutil.rmtree(config_folder, ignore_errors=True)
        os.rename(config_save_folder, config_folder)

@contextmanager
def handle_daemon():
    from aiida.cmdline.verdilib import Daemon
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        Daemon().daemon_restart()
    yield
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        Daemon().daemon_stop()
