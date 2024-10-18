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


@app.route("/users/", methods=["POST"], strict_slashes=False)
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


@app.route("/sessions/", methods=["POST"], strict_slashes=False)
def login() -> flask.Response:
    """
    login route
    """
    email: Optional[str] = flask.request.form.get("email")
    password: Optional[str] = flask.request.form.get("password")

    if not AUTH.valid_login(email, password):
        flask.abort(401)

    session_id: Optional[str] = AUTH.create_session(email)

    if session_id is None:
        flask.abort(401)

    response: flask.Response = flask.make_response(
        flask.jsonify({"email": email, "message": "logged in"})
    )
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
