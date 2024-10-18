#!/usr/bin/env python3
"""
Flask app for signing 'User's in.
"""
from typing import Tuple
import flask

app = flask.Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def bienvenue() -> Tuple[flask.Response, int]:
    """
    Expects GET with nothing,
    responds with {"message": "Bienvenue"} and a status code of 200.
    """
    return flask.jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
