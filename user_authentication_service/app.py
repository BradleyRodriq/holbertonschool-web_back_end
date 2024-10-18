#!/usr/bin/env python3
"""
Flask app for signing 'User's in.
"""
from typing import Tuple, Optional
from sqlalchemy.orm.exc import NoResultFound
import flask
from auth import Auth
from user import User


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


@app.route("/sessions/", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    logout route
    """
    session_id_cookie: Optional[str] = \
        flask.request.cookies.get(
            "session_id"
        )

    if session_id_cookie is None:
        flask.abort(403)

    user: Optional[User] = \
        AUTH.get_user_from_session_id(
            session_id_cookie
        )

    if user is None:
        flask.abort(403)

    try:
        AUTH.destroy_session(user.id)
    except NoResultFound:
        flask.abort(403)

    return flask.redirect(flask.url_for('bienvenue'))


@app.route("/profile/", methods=["GET"], strict_slashes=False)
def profile() -> flask.Response:
    """
    respond to the /profile route
    """
    session_id_cookie: Optional[str] = \
        flask.request.cookies.get(
            "session_id"
        )

    if session_id_cookie is None:
        flask.abort(403)

    user: Optional[User] = \
        AUTH.get_user_from_session_id(
            session_id_cookie
        )

    if user is None:
        flask.abort(403)

    return flask.jsonify({"email": user.email})


@app.route("/reset_password/", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> flask.Response:
    """
    get reset pw token
    """
    email: Optional[str] = flask.request.form.get("email")

    if email is None:
        flask.abort(403)

    try:
        result: str = AUTH.get_reset_password_token(email)
    except ValueError:
        flask.abort(403)

    return flask.jsonify({"email": email, "reset_token": result})


def update_password() -> flask.Response:
    """
    update password endpoint
    """
    email: Optional[str] = flask.request.form.get("email")
    reset_token: Optional[str] = flask.request.form.get("reset_token")
    new_pw: Optional[str] = flask.request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_pw)
    except ValueError:
        flask.abort(403)

    return flask.jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
