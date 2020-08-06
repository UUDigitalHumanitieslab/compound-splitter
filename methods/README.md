Every compound splitter is a folder consisting of at least one run.json file specifying how to run it in a server mode.

```json
{
    "displayName": "Example Splitter",
    "exec": "python run.py",
    "protocol": "exec"
}
```

# Protocols

## module

Place the module in `__init__.py` and specify the function `split(word)`.

## http

The server should work using the following basic protocol (http):

GET /split/{word}

# Output result

All of the protocols should return a JSON, formatted as:

```json
{
    "candidates": [
        {
            "parts": ["compound", "split", "result"],
            "score": 1
        },
        {
            "parts": ["compound", "splitresult"],
            "score": 0
        }
    ]
}
```

Score should be positive: higher should mean more probable/better. If the algorithm doesn't have a scoring method, return 1.
