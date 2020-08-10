from flask import Flask, jsonify

from .splitter import list_methods, get_method, get_method_data

app = Flask(__name__)


@app.route("/split/<method_name>/<compound>")
def get_split(method_name: str, compound: str):
    method = get_method(method_name)
    result = method.split(compound)
    return jsonify(result)


@app.route("/list")
def get_list():
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
