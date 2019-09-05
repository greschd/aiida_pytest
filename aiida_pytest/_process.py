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
        from aiida.plugins import CalculationFactory
        builder = CalculationFactory(calculation_string).get_builder()
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
        from aiida.orm import Code
        builder.code = Code.get_from_string(code_string)
    return inner

@export
@pytest.fixture
def set_single_core():
    def inner(builder):
        builder.metadata.options = dict(
            resources={'num_machines': 1, 'tot_num_mpiprocs': 1},
            withmpi=False
        )
    return inner

# TODO: Check for uses of these fixtures, and if / how they need to be changed.

@export
@pytest.fixture
def assert_state():
    def inner(pid, state):
        from aiida.orm import load_node
        from aiida.engine import ProcessState
        if isinstance(state, ProcessState):
            state = state.value
        calc_node = load_node(pid)
        assert calc_node.get_attribute('process_state') == state
    return inner

@export
@pytest.fixture
def assert_finished(assert_state):
    def inner(pid):
        from aiida.engine import ProcessState
        assert_state(pid, ProcessState.FINISHED)
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
