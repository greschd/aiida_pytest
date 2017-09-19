#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_sample_from_subfolder(sample):
    with open(sample('test.txt'), 'r') as f:
        assert f.read() == 'Test text\n'
