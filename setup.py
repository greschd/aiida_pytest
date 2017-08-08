# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

requirements = [
    'aiida-core',
    'pytest',
    'temporary',
    'pyyaml',
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
        install_requires=requirements,
    )
