# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines a fixture to check if the AiiDA entrypoints (workflows, calculations,
parsers, data, transports) are loadable through the corresponding factory.
"""

import pkg_resources

import pytest
from fsc.export import export


@export
@pytest.fixture
def check_entrypoints(configure):  # pylint: disable=unused-argument
    """
    Fixture to check that loading of all the workflow, calculation and parser
    entrypoints through the corresponding factory works for the given (base)
    module name.
    """
    def inner(module_name):  # pylint: disable=missing-docstring
        from aiida.plugins.factories import WorkflowFactory, CalculationFactory, DataFactory, ParserFactory, TransportFactory
        for entrypoint_name, factory in [
            ('aiida.workflows', WorkflowFactory),
            ('aiida.calculations', CalculationFactory),
            ('aiida.parsers', ParserFactory), ('aiida.data', DataFactory),
            ('aiida.transports', TransportFactory)
        ]:
            for entry_point in pkg_resources.iter_entry_points(
                entrypoint_name
            ):
                if entry_point.module_name.split('.')[0] == module_name:
                    factory(entry_point.name)

    return inner
