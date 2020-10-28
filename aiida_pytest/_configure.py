# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import os
import copy
import shutil
import pathlib
import subprocess
from builtins import input
from contextlib import contextmanager, suppress

import yaml

import aiida
from aiida.manage.tests import get_test_profile_name
from aiida.manage.tests.pytest_fixtures import aiida_profile

import pytest

# Need to export the fixtures that we depend on.
# NOTE: This is a workaround for the incorrect way of using the
# plugin (wildcard import) instead of specifying it as pytest plugin.
__all__ = (
    'aiida_profile', 'pytest_addoption', 'config_dict',
    'get_queue_name_from_code', 'configure_with_daemon', 'configure'
)


def pytest_addoption(parser):
    parser.addoption(
        '--queue-name',
        action='store',
        help='Name of the queue used to submit calculations.'
    )
    parser.addoption(
        '--quiet-wipe',
        action='store_true',
        help='Disable asking for input before wiping the test AiiDA environment.'
    )
    parser.addoption(
        '--print-status',
        action='store_true',
        help='Print the calculation and work status before exiting.'
    )
    parser.addoption(
        '--end-cmd',
        action='store',
        help=
        'Command to run before the tear-down (with output capture suspended).'
    )
    parser.addoption(
        '--aiida-pytest-conf-file',
        action='store',
        help='Path of the aiida-pytest config file to be used.'
    )


@pytest.fixture(scope='session')
def config_dict(request, pytestconfig):
    config_path = pathlib.Path(
        request.config.getoption('--aiida-pytest-conf-file') or 'config.yml'
    )
    if not (config_path.exists() or config_path.is_absolute()):
        config_path = pytestconfig.rootpath / config_path
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    if config is None:
        config = dict()
    return config


@pytest.fixture(scope='session')
def get_queue_name_from_code(request, config_dict):
    def inner(code):
        queue_name = request.config.getoption('--queue-name')
        if queue_name is None:
            computer = config_dict['codes'][code]['remote_computer']
            queue_name = config_dict['computers'][computer]['queue_name']
        return queue_name

    return inner


@pytest.fixture(scope='session')
def configure_with_daemon(configure):
    profile_name = get_test_profile_name()
    if profile_name is not None:
        profile_args = ('-p', profile_name)
    else:
        profile_args = tuple()
    subprocess.run(['verdi', *profile_args, 'daemon', 'start'],
                   env=os.environ,
                   stdout=subprocess.DEVNULL)
    yield
    subprocess.run(['verdi', *profile_args, 'daemon', 'stop'],
                   env=os.environ,
                   stdout=subprocess.DEVNULL)


@pytest.fixture(scope='session')
def configure(pytestconfig, config_dict, aiida_profile):
    aiida_profile.reset_db()
    config = copy.deepcopy(config_dict)
    with suppress(AttributeError):
        os.environ['AIIDA_PATH'] = aiida_profile._manager.root_dir

    from ._computer import setup_computer
    computers = config.get('computers', {})
    for name, kwargs in computers.items():
        setup_computer(
            name=name,
            **{k: v
               for k, v in kwargs.items() if k != 'queue_name'}
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

    # aiida.load_profile()
    yield

    # Handle compatibility break in pytest
    capture_manager = pytestconfig.pluginmanager.getplugin('capturemanager')
    init = getattr(
        capture_manager, 'init_capturings',
        getattr(capture_manager, 'start_global_capturing', None)
    )
    suspend = getattr(
        capture_manager, 'suspendcapture',
        getattr(capture_manager, 'suspend_global_capture', None)
    )
    resume = getattr(
        capture_manager, 'resumecapture',
        getattr(capture_manager, 'resume_global_capture', None)
    )

    @contextmanager
    def suspend_capture():
        with suppress(AssertionError):
            init()
        suspend(in_=True)
        yield
        resume()

    if pytestconfig.option.print_status:
        with suspend_capture():
            print('\n\nProcess List:')
            subprocess.call(['verdi', 'process', 'list', '-a'])
    end_cmd = pytestconfig.option.end_cmd
    if end_cmd is not None:
        with suspend_capture():
            print("Executing '{}'".format(end_cmd))
            subprocess.call(end_cmd, shell=True)

    if not pytestconfig.option.quiet_wipe:
        with suspend_capture():
            print("\n")
            with suppress(AttributeError):
                print(
                    'AiiDA root directory: {}'.format(
                        aiida_profile._manager.root_dir
                    )
                )
            input(
                "Tests finished. Press enter to wipe the test AiiDA environment."
            )


@contextmanager
def reset_after_run():
    config_folder = os.path.expanduser(
        aiida.manage.configuration.settings.AIIDA_CONFIG_FOLDER
    )
    config_save_folder = os.path.join(
        os.path.dirname(config_folder), '.aiida~'
    )
    reset_config(config_folder, config_save_folder)
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
