import time

import pytest
from fsc.export import export

@export
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

@export
@pytest.fixture
def inputs_setup(set_code, set_single_core):
    def inner(inputs, code_string, single_core=True):
        set_code(inputs, code_string=code_string)
        if single_core:
            set_single_core(inputs)
    return inner

@export
@pytest.fixture
def set_code():
    def inner(inputs, code_string):
        from aiida.orm.code import Code
        inputs.code = Code.get_from_string(code_string)
    return inner

@export
@pytest.fixture
def set_single_core():
    def inner(inputs):
        inputs._options.resources = {'num_machines': 1, 'tot_num_mpiprocs': 1}
        inputs._options.withmpi = False
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
                assert calc.has_finished_ok()
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
        while not calc.has_finished():
            time.sleep(timeout)
    return inner
