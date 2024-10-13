#!/usr/bin/env python3
"""
Contains the flask route '/api/v1/auth_session/login/',
which allows the user to login for the first time,
and creates a new session for the user.
"""
from typing import List
import os
import flask
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """
    login route
    """
    from api.v1.app import auth
    email = flask.request.form.get("email", default=None)
    password = flask.request.form.get("password", default=None)

    if email is None:
        return flask.jsonify({"error": "email missing"}), 400

    if password is None:
        return flask.jsonify({"error": "password missing"}), 400

    users_with_email: List[User] = User.search({"email": email})

    if not users_with_email:
        return flask.jsonify({"error": "no user found for this email"}), 404

    assert len(users_with_email) == 1

    user = users_with_email[0]

    if not user.is_valid_password(password):
        return flask.jsonify({"error": "wrong password"}), 401

    assert isinstance(auth, SessionAuth)

    session_id = auth.create_session(user.id)

    session_cookie: str = os.environ.get("SESSION_NAME")

    response: flask.Response = flask.make_response(
        flask.jsonify(user.to_json())
    )
    response.set_cookie(session_cookie, session_id)

    return response
