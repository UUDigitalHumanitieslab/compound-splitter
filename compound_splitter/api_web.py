from flask import Flask, jsonify
from .splitter import list_methods, get_method

app = Flask(__name__)


@app.route("/split/<method_name>/<compound>")
def get_split(method_name: str, compound: str):
    method = get_method(method_name)
    result = method.split(compound)
    return jsonify(result)


@app.route("/list")
def get_list():
    methods = list_methods()
    return jsonify(methods)


if __name__ == '__main__':
    app.run()
