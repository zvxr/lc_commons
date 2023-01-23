import lc_commons

from setuptools import setup, find_packages


setup(
    name="lc_commons",
    version=lc_commons.__version__,
    author="Mike McConnell",
    author_email="djrahl84+lc_commons@gmail.com",
    description=("P2P Loan Data Collector"),
    url="https://github.com/zvxr/lc_commons",
    packages=find_packages(),
)
