"""Install parameters for CLI and python import."""
from sys import version_info
from setuptools import setup
import logging

logging.getLogger().setLevel(logging.DEBUG)

if version_info < (3, 7):
    raise ImportError("This module requires Python >=3.7.  Use 0.3.1 for Python3.6")

with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name="watlow",
    version="0.5.1",
    description="Python driver for Watlow EZ-Zone temperature controllers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://github.com/numat/watlow/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    packages=["watlow"],
    install_requires=[
        'pymodbus @ git+ssh://git@github.com/pymodbus-dev/pymodbus@97ffffc9e7dc164161dae936782c49d7dae8a7de#egg=pymodbus',
        "pyserial",
        "crcmod"],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
        ],
    },
    entry_points={
        "console_scripts": [("watlow = watlow:command_line")]
    },
    license="GPLv2",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ]
)
