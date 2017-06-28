# -*- coding: utf-8 -*-
"""
setup: usage: pip install -e .[graphs]
"""

import sys
from setuptools import setup, find_packages

requirements = [
    'aiida-core',
    'pytest',
    'temporary',
    'pyyaml'
]
if sys.version_info < (3,):
    requirements += ['chainmap']

if __name__ == '__main__':
    setup(
        name='aiida-pytest',
        version='0.0.0a1',
        description='Module to simplify using pytest for AiiDA plugins',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        license='GPL',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: AiiDA',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='pytest aiida workflows',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        install_requires=requirements,
    )
