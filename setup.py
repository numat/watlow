"""Install parameters for CLI and python import."""
from setuptools import setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name="watlow",
    version="0.6.2",
    description="Python driver for Watlow EZ-Zone temperature controllers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/numat/watlow/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    maintainer="Alex Ruddick",
    maintainer_email="alex@numat-tech.com",
    packages=["watlow"],
    install_requires=[
        'pymodbus>=2.4.0; python_version == "3.8"',
        'pymodbus>=2.4.0; python_version == "3.9"',
        'pymodbus>=3.0.2,<3.7.0; python_version >= "3.10"',
        "pyserial",
        "crcmod"],
    extras_require={
        'test': [
            'mypy==1.14.1',
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
            'ruff==0.4.7',
            'types-pyserial',
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ]
)
