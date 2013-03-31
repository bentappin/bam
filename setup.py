# encoding: utf-8
from setuptools import setup, find_packages

import bam


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.rst') as f:
    license = f.read()


setup(
    name='bam',
    version=bam.__version__,
    description="Text snippets on the command line.",
    long_description=readme,
    author='Ben Tappin',
    author_email='ben@mrben.co.uk',
    license=license,
    install_requires=['clint>=0.3.1'],
    packages=['bam'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ),
    entry_points={
        'console_scripts': [
            'bam = bam.command:main',
        ],
    }
)
