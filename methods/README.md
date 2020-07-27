Every compound splitter is a folder consisting of at least one run.json file specifying how to run it in a server mode.

```json
{
    "displayName": "Example Splitter",
    "exec": "python run.py" /* relative to root of split folder */
}
```

The server should work using the following basic protocol (http):

GET /split/{word}

And return a JSON

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
}}
```

Score should be positive: higher should mean more probable/better. If the algorithm doesn't have a scoring method, return 1.
