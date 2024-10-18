#!/usr/bin/env python3
"""
Flask app for signing 'User's in.
"""
from typing import Tuple, Optional
import flask
from auth import Auth


app = flask.Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def bienvenue() -> Tuple[flask.Response, int]:
    """
    responds with Bienevue
    """
    return flask.jsonify({"message": "Bienvenue"}), 200


def users() -> Tuple[flask.Response, int]:
    """
    users route
    """
    email: Optional[str] = flask.request.form.get("email")
    password: Optional[str] = flask.request.form.get("password")

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return flask.jsonify({"message": "email already registered"}), 400
    else:
        return flask.jsonify({"email": email, "message": "user created"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
