from typing import cast, Any

import os
import json
import importlib

base_path = os.path.dirname(os.path.dirname(__file__))
METHODS_DIR = os.path.join(base_path, 'methods')


class Module:
    '''
    Object representing a python module with compound splitting functions.
    '''

    def __init__(self, name: str, run_data):
        self.module = cast(Any, importlib.import_module(f"methods.{name}"))

    def split(self, compound: str):
        '''
        Split a compound.

        Calls the `split` function of the method. If this is correctly
        implemented, this returns a dict with key `"candidates"`, which contains
        an array.

        Each candidate is a dict with two keys:
        - `"parts"`: an array of parts in the compound
        - `"score"`: score of this split

        Methods may return multiple candidates with different scores.
        '''
        return self.module.split(compound)

    def start(self):
        '''
        Start-up for this method
        (e.g. import data, start a socket server, etc.)
        '''
        self.module.start()

    def stop(self):
        '''
        Teardown for this method
        '''
        self.module.stop()

    def prepare(self):
        self.module.prepare()


def get_method_data(name: str):
    '''
    Load the JSON configuration file for a method.

    Opens the `run.json` file in the method directory
    and returns its contents.
    '''

    with open(os.path.join(METHODS_DIR, name, 'run.json')) as run_json:
        return json.load(run_json)


def get_method(name: str):
    '''
    Return a method as a python module.

    Input must be the name of the method.

    Output is a python object with `split`, `start`,
    `stop`, and `prepare` methods.
    '''

    run_data = get_method_data(name)
    method = {
        'module': Module(name, run_data)
    }[run_data['protocol']]

    return method


def list_methods():
    '''
    List every python module in the "methods" directory

    Collects all directories in the "methods" directory,
    and read the JSON configuration for each. Returns a dict
    with metadata for each method.
    '''

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
