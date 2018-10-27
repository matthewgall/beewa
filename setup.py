"""A setuptools based setup module for beewa
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# And get version information from the Makefile
with open(path.join(here, 'Makefile'), encoding='utf-8') as f:
    version = re.findall('VERSION\s\:\=\s([\d.]*)', f.read())[0]

setup(
    name='beewa',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='beewa makes controlling your hivehome.com powered system easy!',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/matthewgall/beewa',

    # Author details
    author='Matthew Gall',
    author_email='git@matthewgall.com',

    # Choose your license
    license='MIT',

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='linux',
    
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project?
        'Development Status :: 4 - Beta',

        # And environment
        'Environment :: Console',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'beewa = beewa.cli:main',
            'hive = beewa.cli:main'
        ],
    },
    install_requires=['requests']
)
