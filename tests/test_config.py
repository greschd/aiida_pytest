#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def test_configure_from_file(configure_from_file):
    configure_from_file(os.path.abspath('config.yml'))
