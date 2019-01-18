#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

def test_sample(sample):
    with open(sample('test.txt'), 'r') as f:
        assert f.read() == 'Test text\n'
