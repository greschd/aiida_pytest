#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aiida.work import ObjectLoader

from .contextmanagers import redirect_stdout

def setup_pseudo_family(command_name, folder, group_name, group_description):
    pseudo_cmd = ObjectLoader().load_object(command_name)()
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        pseudo_cmd.uploadfamily(folder, group_name, group_description)
