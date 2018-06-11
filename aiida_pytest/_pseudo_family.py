#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aiida.common.utils import get_object_from_string

from .contextmanagers import redirect_stdout

def setup_pseudo_family(command_name, folder, group_name, group_description):
    pseudo_cmd = get_object_from_string(command_name)()
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        pseudo_cmd.uploadfamily(folder, group_name, group_description)
