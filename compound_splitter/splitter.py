from typing import cast, Any

import os
import json
import importlib

from flask import Flask, jsonify
app = Flask(__name__)

METHODS_DIR = 'methods'


class Module:
    def __init__(self, name: str, run_data):
        self.module = cast(Any, importlib.import_module(f"methods.{name}"))

    def split(self, compound: str):
        return self.module.split(compound)


def get_method_data(name: str):
    with open(os.path.join(METHODS_DIR, name, 'run.json')) as run_json:
        return json.load(run_json)


def get_method(name: str):
    run_data = get_method_data(name)
    method = {
        'module': Module(name, run_data)
    }[run_data['protocol']]

    return method


@app.route("/split/<method_name>/<compound>")
def split(method_name: str, compound: str):
    method = get_method(method_name)
    result = method.split(compound)
    return jsonify(result)


@app.route("/list")
def list_methods():
    methods = []
    for name in os.listdir(METHODS_DIR):
        if os.path.isdir(os.path.join(METHODS_DIR, name)):
            methods += [{
                "name": name,
                **get_method_data(name)
            }]
    return jsonify(methods)


if __name__ == '__main__':
    app.run()
