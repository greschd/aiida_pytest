from __future__ import division, print_function, unicode_literals

import os
import copy
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

__all__ = ['configure', 'configure_with_daemon', 'pytest_addoption', 'queue_name_from_code', 'config_dict']

def pytest_addoption(parser):
    parser.addoption('--queue-name', action='store', help='Name of the queue used to submit calculations.')
    parser.addoption('--quiet-wipe', action='store_true', help='Disable asking for input before wiping the test AiiDA environment.')

@pytest.fixture(scope='session')
def config_dict():
    with open(os.path.abspath('config.yml'), 'r') as f:
        config = yaml.load(f)
    if config is None:
        config = dict()
    return config

@pytest.fixture(scope='session')
def queue_name_from_code(request, config_dict):
    def inner(code):
        queue_name = request.config.getoption('--queue-name')
        if queue_name is None:
            computer = config_dict['codes'][code]['remote_computer']
            queue_name = config_dict['computers'][computer]['queue_name']
        return queue_name
    return inner

@pytest.fixture(scope='session')
def configure_with_daemon(configure):
    with handle_daemon():
        yield

@pytest.fixture(scope='session')
def configure(pytestconfig, config_dict):
    config = copy.deepcopy(config_dict)
    with temporary.temp_dir() as td, PGTest(max_connections=100) as pgt:
        with reset_after_run():
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
            computers = config.get('computers', {})
            for name, kwargs in computers.items():
                setup_computer(
                    name=name,
                    **{k: v for k, v in kwargs.items() if k != 'queue_name'}
                )

            from ._code import setup_code
            codes = config.get('codes', {})
            for label, kwargs in codes.items():
                setup_code(label=label, **kwargs)

            # with same pattern setup test psf- pseudo family
            from ._pseudo_family import setup_pseudo_family
            pseudo_families = config.get('pseudo_families', {})
            for group_name, kwargs in pseudo_families.items():
                setup_pseudo_family(group_name=group_name, **kwargs)

            yield
            if not pytestconfig.option.quiet_wipe:
                capture_manager = pytest.config.pluginmanager.getplugin('capturemanager')
                try:
                    capture_manager.init_capturings()
                except AssertionError:
                    pass
                capture_manager.suspendcapture(in_=True)
                raw_input("\nTests finished. Press enter to wipe the test AiiDA environment.")
                capture_manager.resumecapture()

@contextmanager
def reset_after_run():
    config_folder = os.path.expanduser(aiida.common.setup.AIIDA_CONFIG_FOLDER)
    config_save_folder = os.path.join(
        os.path.dirname(config_folder), '.aiida~'
    )
    reset_config(config_folder, config_save_folder)
    assert not os.path.isfile(os.path.join(config_folder, 'config.json'))
    shutil.copytree(config_folder, config_save_folder)
    try:
        yield
    except Exception as e:
        raise e
    finally:
        reset_config(config_folder, config_save_folder)
        reset_submit_test_folder(config_folder)


def reset_config(config_folder, config_save_folder):
    if os.path.isdir(config_save_folder):
        shutil.rmtree(config_folder, ignore_errors=True)
        os.rename(config_save_folder, config_folder)


def reset_submit_test_folder(config_folder):
    submit_test_folder = os.path.join(
        os.path.dirname(config_folder), 'submit_test'
    )
    if os.path.isdir(submit_test_folder):
        # remove temp `submit_test` folder for not_submitted_to_daemon tests
        shutil.rmtree(submit_test_folder)


@contextmanager
def handle_daemon():
    from aiida.cmdline.verdilib import Daemon
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        Daemon().daemon_restart()
    try:
        yield
    except Exception as e:
        raise e
    finally:
        with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
            Daemon().daemon_stop()
