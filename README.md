# Compound Splitter

[![DOI](https://zenodo.org/badge/282840038.svg)](https://zenodo.org/badge/latestdoi/282840038)

This is a basic wrapper for multiple Dutch compound splitters. The purpose of this wrapper is to:

- provide a unified API for multiple compound splitters. The package offers a simple socket server and a Flask application for this purpose.
- evaluate the accuracy of different compound splitters

## Intended audience

The package was initially developed for [T-scan](https://github.com/UUDigitalHumanitieslab/tscan), a natural language analysis application intended for research. For T-scan, we required that users could choose between different algorithms (hence the need for a unified API), and some evaluation of the quality of those algorithms.

The resulting package is useful if you want to run a compound splitting service (e.g. as part of an API or web application), or if you want to evaluate compound splitter methods. Adding new methods, even ones that are not python packages, should be feasible if you have programming experience.

If you are looking for a simple, lightweight python package for compound splitting, this is not it. [compound-word-splitter](https://github.com/TimKam/compound-word-splitter) may be a good alternative for you.

## Compound splitting methods

The following compound splitters are included:

- `compound-splitter-nl`, developed by Katja Hoffman, Valentin Jijkoun, Jaap Kamps, and Christof Monz (LGPL-3.0 license). See https://web.archive.org/web/20200813005715/https://ilps.science.uva.nl/resources/compound-splitter-nl/ for the archived website and https://github.com/bminixhofer/ilps-nl-splitter for an archive of the source code.
- SECOS, developed by Martin Riedel and Chris Biemann (Apache-2.0 license). See https://github.com/riedlma/SECOS 
- MCS, developed by Patrick Ziering. See https://www.ims.uni-stuttgart.de/en/research/resources/tools/mcs/

As a baseline, we also include a "never" algorithm, which never splits.

## Requirements

- Python 3.8+
- Java (only required for MCS)

## Installation

### Installing with pip

`compound-splitters-nl` is available as a python package, which includes all the data for all included compound splitter methods. This complete package is too large to be registered on PyPI, but you can download the package from our [releases](https://github.com/UUDigitalHumanitieslab/compound-splitter/releases/).

The archived package can be installed via pip by installing the local file:

```bash
pip install compound-splitters-nl-*.tar.gz
# or substitute with your file path
```

If you want to use the web API, you will need to install additional dependencies:

```bash
pip install compound-splitters-nl-*.tar.gz[web_api]
```

### Installing from source code

You can also clone the source code repository. In this case, you will still need to download and unpack the data needed for the compound splitter methods. Run installation with:

``` bash
pip install -r requirements.txt
python retrieve.py
python prepare.py
```

## Tests

``` bash
python -m unittest discover tests/
```

## Evaluate Different Compound Algorithms

This will evaluate the different algorithms using the reference files in `test_sets` .

``` bash
python -m compound_splitter.evaluate
```

## Run Web API

``` bash
python -m compound_splitter.api_web
```

### JSON Interface

 `GET /list`

Lists the splitting methods.

 `GET /split/<method_name>/<compound>`

Splits the compound using the specified method.

## Run Simple Socket Server

``` bash
python -m compound_splitter.socket_server
```

``` bash
$ telnet localhost 7005
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
bedrijfsaansprakelijkheidsverzekering,secos
bedrijfs,aansprakelijkheids,verzekeringConnection closed by foreign host.
```

## Install

Make sure the requirements are installed and prepared ( `prepare.py` ).

``` bash
pip install -e .
compound-splitters-nl-api # starts the web API
compound-splitters-nl-socket # start the socket server
```
