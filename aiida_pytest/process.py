#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

@pytest.fixture
def get_process_inputs(inputs_setup):
    def inner(calculation_string, code_string, single_core=True):
        from aiida.orm import CalculationFactory
        process = CalculationFactory(calculation_string).process()
        inputs = process.get_inputs_template()
        inputs_setup(
            inputs,
            code_string=code_string,
            single_core=single_core
        )
        return process, inputs
    return inner

@pytest.fixture
def inputs_setup(set_code, set_single_core):
    def inner(inputs, code_string, single_core=True):
        set_code(inputs, code_string=code_string)
        if single_core:
            set_single_core(inputs)
    return inner

@pytest.fixture
def set_code():
    def inner(inputs, code_string):
        from aiida.orm.code import Code
        inputs.code = Code.get_from_string(code_string)
    return inner

@pytest.fixture
def set_single_core():
    def inner(inputs):
        inputs._options.resources = {'num_machines': 1, 'tot_num_mpiprocs': 1}
        inputs._options.withmpi = False
    return inner
