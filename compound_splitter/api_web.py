from typing import cast, Dict
from flask import Flask, jsonify
from .splitter import list_methods, get_method, Module

app = Flask(__name__)
'''
A simple flask app that handles compound splitting requests
'''

started_methods = cast(Dict[str, Module], {})


@app.route("/split/<method_name>/<compound>")
def get_split(method_name: str, compound: str):
    '''
    Split a compound with the specified method.

    If this is the first time the method is called
    during runtime, run its `start` method.
    '''
    
    if method_name in started_methods:
        method = started_methods[method_name]
    else:
        method = get_method(method_name)
        method.start()
        started_methods[method_name] = method
    result = method.split(compound)
    return jsonify(result)


@app.route("/list")
def get_list():
    '''
    Return an array of all available methods.
    '''
    
    methods = list_methods()
    return jsonify(methods)


def cleanup():
    '''
    Execute teardown for each method that has 
    been started up.
    '''

    for method in started_methods.values():
        method.stop()


def main():
    try:
        app.run()
    finally:
        cleanup()


if __name__ == '__main__':
    main()
