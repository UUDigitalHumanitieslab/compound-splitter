# Compound Splitter

This is a basic wrapper for multiple Dutch compound splitters.

## Requirements

Python 3.6+

``` bash
pip install -r requirements.txt
python retrieve.py
```

## Tests

``` bash
python -m unittest discover tests/
```

## Evaluate Different Compound Algorithms

This will evaluate the different algorithms using the reference files in `test_sets`.

```bash
python -m compound_splitter.evaluate
```

## Run Web API

```bash
python -m compound_splitter.api_web
```

### JSON Interface

`GET /list`

Lists the splitting methods.

`GET /split/<method_name>/<compound>`

Splits the compound using the specified method.

## Run Simple Socket Server

```bash
python -m compound_splitter.socket_server
```

```bash
$ telnet localhost 7005
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
bedrijfsaansprakelijkheidsverzekering,secos
bedrijfs,aansprakelijkheids,verzekeringConnection closed by foreign host.
```
