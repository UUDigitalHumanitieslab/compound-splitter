``` bash
pip install -r requirements.txt
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
