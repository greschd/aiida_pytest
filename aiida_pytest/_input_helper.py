#!/usr/bin/env python
# -*- coding: utf-8 -*-

class InputHelper:
    """
    Class to mock a given input. This is needed because io.StringIO cannot create the EOFError needed to end multiline inputs in AiiDA (Ctrl+D).
    """
    def __init__(self, input):
        self.input = input

    def readline(self):
        try:
            res = self.input.pop(0)
            if res is None:
                raise EOFError
            return res + '\n'
        except IndexError:
            raise EOFError
