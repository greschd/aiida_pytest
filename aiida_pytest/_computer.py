#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass

from click.testing import CliRunner
from aiida.cmdline.commands.cmd_computer import setup_computer as _setup_computer, computer_configure as _configure_computer


def setup_computer(name,
                   hostname,
                   transport,
                   scheduler,
                   work_directory,
                   shebang='#!/bin/bash',
                   configuration={'username': getpass.getuser()},
                   description='',
                   mpirun_command='mpirun -np {tot_num_mpiprocs}',
                   num_cpus=1,
                   enabled=True,
                   prepend_text=None,
                   append_text=None):
    runner = CliRunner()
    runner.invoke(
        _setup_computer,
        name=name,
        hostname=hostname,
        description=description,
        work_dir=work_directory,
        shebang=shebang,
        mpirun_command=mpirun_command,
        enabled=enabled,
        mpiprocs_per_machine=num_cpus,
        prepend_text=prepend_text,
        append_text=append_text,
        non_interactive=True,
    )
    runner.invoke(_configure_computer.commands[transport], name=name, **configuration)
