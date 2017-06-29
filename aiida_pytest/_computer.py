#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aiida.cmdline.verdilib import Computer

from ._input_helper import InputHelper
from ._contextmanagers import redirect_stdin, redirect_stdout

def setup_computer(
        name,
        hostname,
        transport,
        scheduler,
        work_directory,
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
        # TODO: Implement computers which need configuring
        Computer().computer_configure(name)
