#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="compound-splitters-nl",
    version="0.0.1",
    author="Sheean Spoel, Luka van der Plas",
    author_email="s.j.j.spoel@uu.nl",
    description="Wrapper and evaluation service for multiple Dutch compound splitters",
    keywords="compound splitter nlp computational_linguistics dutch",
    url="https://github.com/UUDigitalHumanitieslab/compound-splitter",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3.7",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        'License :: OSI Approved :: BSD License',
    ],
    package_data = {'methods':['*/bin/**/*'] },
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=['Flask',
                      'pytest',
                      'requests'],
    entry_points={
        'console_scripts': [
            'compound-splitters-nl-api = compound_splitter.api_web:main'
            'compound-splitters-nl-socket = compound_splitter.socket_server:main'
        ]
    }
)
