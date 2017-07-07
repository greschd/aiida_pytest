#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import getpass

from aiida.cmdline.verdilib import Computer

from ._input_helper import InputHelper
from .contextmanagers import redirect_stdin, redirect_stdout

def setup_computer(
        name,
        hostname,
        transport,
        scheduler,
        work_directory,
        configuration={'username': getpass.getuser()},
        description='',
        mpirun_command='mprun -np {tot_num_mpiprocs}',
        num_cpus=1,
        enabled=True,
):
    computer_input = InputHelper(input=[
        name,
        hostname,
        description,
        str(enabled),
        transport,
        scheduler,
        work_directory,
        mpirun_command,
        str(num_cpus),
        None,
        None
    ])
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        with redirect_stdin(computer_input):
            Computer().computer_setup()
    if transport == 'local':
        configure_localhost(name)
    else:
        configure_computer(name, **configuration)

def configure_localhost(name):
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        Computer().computer_configure(name)

def configure_computer(
    name,
    username='',
    port=22,
    look_for_keys=True,
    key_filename='',
    timeout=60,
    allow_agent=True,
    proxy_command='',
    compress=True,
    gss_auth=False,
    gss_kex=False,
    gss_deleg_creds=False,
    gss_host='',
    load_system_host_keys=True,
    key_policy='RejectPolicy',
):
    configure_input = InputHelper(input=[
        username,
        str(port),
        str(look_for_keys),
        key_filename,
        str(timeout),
        str(allow_agent),
        proxy_command,
        str(compress),
        str(gss_auth),
        str(gss_kex),
        str(gss_deleg_creds),
        str(gss_host),
        str(load_system_host_keys),
        key_policy
    ])
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        with redirect_stdin(configure_input):
            Computer().computer_configure(name)
