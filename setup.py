"""Install parameters for CLI and python import."""
from sys import version_info
from setuptools import setup

if version_info < (3, 6):
    raise ImportError("This module requires Python >=3.6 for asyncio support")
if version_info >= (3, 10):
    raise ImportError("This module depends on pymodbus, which is incompatible with Python 3.10")

with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name="watlow",
    version="0.3.0",
    description="Python driver for Watlow EZ-Zone temperature controllers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://github.com/numat/watlow/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    packages=["watlow"],
    install_requires=["pymodbus>=2.4.0",
                      "pyserial",
                      "crcmod"],
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ]
)
