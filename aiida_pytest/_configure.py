# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import os
import copy
import shutil
import subprocess32 as subprocess
from builtins import input
from contextlib import contextmanager

import yaml

import aiida
from aiida.manage.tests.pytest_fixtures import aiida_profile

import pytest
from fsc.export import export

# from .contextmanagers import redirect_stdout

__all__ = ['aiida_profile'] # Need to export the fixtures that we depend on.

@export
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


@export
@pytest.fixture(scope='session')
def config_dict():
    with open(os.path.abspath('config.yml'), 'r') as f:
        config = yaml.load(f)
    if config is None:
        config = dict()
    return config


@export
@pytest.fixture(scope='session')
def get_queue_name_from_code(request, config_dict):
    def inner(code):
        queue_name = request.config.getoption('--queue-name')
        if queue_name is None:
            computer = config_dict['codes'][code]['remote_computer']
            queue_name = config_dict['computers'][computer]['queue_name']
        return queue_name

    return inner


@export
@pytest.fixture(scope='session')
def configure_with_daemon(configure):
    subprocess.run(['verdi', 'daemon', 'start'],
                   env=os.environ,
                   stdout=subprocess.DEVNULL)
    yield
    subprocess.run(['verdi', 'daemon', 'stop'],
                   env=os.environ,
                   stdout=subprocess.DEVNULL)


@export
@pytest.fixture(scope='session')
def configure(pytestconfig, config_dict, aiida_profile):
    config = copy.deepcopy(config_dict)
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
    capture_manager = pytestconfig.pluginmanager.getplugin(
        'capturemanager'
    )
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
        try:
            init()
        except AssertionError:
            pass
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
            print('\nAiiDA root directory: {}'.format(aiida_profile._manager.root_dir))
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
