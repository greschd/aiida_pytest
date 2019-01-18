# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import time

import pytest
from fsc.export import export

@export
@pytest.fixture
def get_process_builder(inputs_setup):
    def inner(calculation_string, code_string, single_core=True):
        from aiida.orm import CalculationFactory
        process = CalculationFactory(calculation_string).process()
        builder = process.get_builder()
        inputs_setup(
            builder,
            code_string=code_string,
            single_core=single_core
        )
        return builder
    return inner

@export
@pytest.fixture
def inputs_setup(set_code, set_single_core):
    def inner(builder, code_string, single_core=True):
        set_code(builder, code_string=code_string)
        if single_core:
            set_single_core(builder)
    return inner

@export
@pytest.fixture
def set_code():
    def inner(builder, code_string):
        from aiida.orm.code import Code
        builder.code = Code.get_from_string(code_string)
    return inner

@export
@pytest.fixture
def set_single_core():
    def inner(builder):
        builder.options = dict(
            resources={'num_machines': 1, 'tot_num_mpiprocs': 1},
            withmpi=False
        )
    return inner

@export
@pytest.fixture
def assert_state():
    def inner(pid, state):
        from aiida.orm import load_node
        from aiida.common.datastructures import calc_states
        from aiida.orm.calculation.work import WorkCalculation
        calc = load_node(pid)
        if isinstance(calc, WorkCalculation):
            if state == calc_states.FINISHED:
                assert calc.exit_status == 0
            else:
                raise ValueError('Cannot check WorkCalculation for state {}'.format(state))
        else:
            assert calc.get_state() == state
    return inner

@export
@pytest.fixture
def assert_finished(assert_state):
    def inner(pid):
        from aiida.common.datastructures import calc_states
        assert_state(pid, calc_states.FINISHED)
    return inner

@export
@pytest.fixture
def wait_for():
    def inner(pid, timeout=1):
        from aiida.orm import load_node
        calc = load_node(pid)
        while not calc.is_terminated:
            time.sleep(timeout)
    return inner
