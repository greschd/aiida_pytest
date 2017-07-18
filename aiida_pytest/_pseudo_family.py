#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from plum.util import load_class

from .contextmanagers import redirect_stdout

def setup_pseudo_family(command_name, folder, group_name, group_description):
    pseudo_cmd = load_class(command_name)()
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        pseudo_cmd.uploadfamily(folder, group_name, group_description)
