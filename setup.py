"""
Setup script for banking-transactions-api package.

This setup.py is maintained for backwards compatibility with setuptools-based tools.
Configuration is primarily in pyproject.toml.
"""

from setuptools import setup, find_packages

setup(
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
)
