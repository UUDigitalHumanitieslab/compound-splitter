# Compound Splitter

This is a basic wrapper for multiple Dutch compound splitters. The purpose of this wrapper is to:

- provide a unified API for multiple compound splitters. The package offers a simple socket server and a Flask application for this purpose.
- evaluate the accuracy of different compound splitters

The following compound splitters are included:

- `compound-splitter-nl`, developed by Katja Hoffman, Valentin Jijkoun, Jaap Kamps, and Christof Monz (LGPL-3.0 license). See https://web.archive.org/web/20200813005715/https://ilps.science.uva.nl/resources/compound-splitter-nl/ for the archived website and https://github.com/bminixhofer/ilps-nl-splitter for an archive of the source code.
- SECOS, developed by Martin Riedel and Chris Biemann (Apache-2.0 license). See https://github.com/riedlma/SECOS 
- MCS, developed by Patrick Ziering. See https://www.ims.uni-stuttgart.de/en/research/resources/tools/mcs/

As a baseline, we also include a "never" algorithm, which never splits.

## Requirements

- Python 3.6+
- Java (only required for MCS)

Quick install:

``` bash
pip install -r requirements.txt
python retrieve.py
python prepare.py
```

This will download and unpack all algorithms.

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
python setup.py install
compound-splitters-nl-api # starts the web API
compound-splitters-nl-socket # start the socket server
```
