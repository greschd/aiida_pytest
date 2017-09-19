# -*- coding: utf-8 -*-

import re
import sys
from setuptools import setup, find_packages

# Get the version number
with open('./aiida_pytest/__init__.py') as f:
    match_expr = "__version__[^'\"]+(['\"])([^'\"]+)"
    version = re.search(match_expr, f.read()).group(2).strip()

if __name__ == '__main__':
    setup(
        name='aiida-pytest',
        version=version,
        description='Module to simplify using pytest for AiiDA plugins',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: AiiDA',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='pytest aiida workflows',
        packages=find_packages(exclude=['aiida', 'plum']),
        include_package_data=True,
        install_requires=[
            'aiida-core',
            'pytest',
            'temporary',
            'pyyaml',
            'fsc.export',
        ],
        extras_require={
            ':python_version < "3"': ['chainmap']
        }
    )
