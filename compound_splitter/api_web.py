from flask import Flask, jsonify
from .splitter import list_methods, get_method

app = Flask(__name__)

started_methods = {}


@app.route("/split/<method_name>/<compound>")
def get_split(method_name: str, compound: str):
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
    methods = list_methods()
    return jsonify(methods)


def cleanup():
    for method in started_methods.values():
        method.stop()


if __name__ == '__main__':
    try:
        app.run()
    finally:
        cleanup()
