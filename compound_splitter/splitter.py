from typing import cast, Any

import os
import json
import importlib

base_path = os.path.dirname(os.path.dirname(__file__))
METHODS_DIR = os.path.join(base_path, 'methods')


class Module:
    def __init__(self, name: str, run_data):
        self.module = cast(Any, importlib.import_module(f"methods.{name}"))

    def split(self, compound: str):
        return self.module.split(compound)

    def start(self):
        self.module.start()

    def stop(self):
        self.module.stop()

    def prepare(self):
        self.module.prepare()


def get_method_data(name: str):
    with open(os.path.join(METHODS_DIR, name, 'run.json')) as run_json:
        return json.load(run_json)


def get_method(name: str):
    run_data = get_method_data(name)
    method = {
        'module': Module(name, run_data)
    }[run_data['protocol']]

    return method


def list_methods():
    methods = []
    for name in os.listdir(METHODS_DIR):
        if name == "__pycache__":
            continue
        if os.path.isdir(os.path.join(METHODS_DIR, name)):
            methods += [{
                "name": name,
                **get_method_data(name)
            }]
    return methods
