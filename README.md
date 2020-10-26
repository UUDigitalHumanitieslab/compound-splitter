# On first use

The MCS splitter requires a Java installation.

All methods:

``` bash
pip install -r requirements.txt
python retrieve.py
```

# Tests

``` bash
python -m unittest discover tests/
```

# Evaluate Different Compound Algorithms

This will evaluate the different algorithms using the reference files in `test_sets`.

```bash
python -m compound_splitter.evaluate
```

# Run web API

```bash
python -m compound_splitter.api_web
```

# Run socket server
```bash
python -m compound_splitter.socket_server
```