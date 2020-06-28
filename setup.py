"""Install parameters for CLI and python import."""
from setuptools import setup

with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name="watlow",
    version="0.2.2",
    description="Python driver for Watlow EZ-Zone temperature controllers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://github.com/numat/watlow/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    packages=["watlow"],
    install_requires=["pymodbus==2.2.0rc1", "pyserial", "crcmod"],
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
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ]
)
