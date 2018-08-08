#!/usr/bin/env python
# -*- coding: utf-8 -*-


from click.testing import CliRunner
from aiida.cmdline.commands.cmd_setup import setup as _setup
from aiida.cmdline.commands.cmd_profile import profile_setdefault

from ._chainmap import ChainMap

def run_setup(**kwargs):
    runner = CliRunner()
    defaults = {
        'backend': 'django',
        'email': 'aiida@localhost',
        'first_name': 'Test',
        'last_name': 'User',
        'institution': 'Test Lab',
        'non_interactive': True,
        'only_config': False,
        'db_host': 'localhost'
    }

    runner.invoke(_setup, **ChainMap(kwargs, defaults))
    runner.invoke(profile_setdefault, profile_name=kwargs['profile'])
