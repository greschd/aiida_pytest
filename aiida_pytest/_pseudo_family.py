#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import os

from aiida.common.utils import get_object_from_string

from .contextmanagers import redirect_stdout


def setup_pseudo_family(command_name, folder, group_name, group_description):
    pseudo_uploadfamily_cmd = get_object_from_string(command_name)
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        pseudo_uploadfamily_cmd.callback(
            path=folder,
            name=group_name,
            description=group_description,
            stop_if_existing=False,
            dry_run=False)
