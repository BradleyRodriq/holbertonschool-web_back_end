#!/usr/bin/env python3
"""
Contains the flask route '/api/v1/auth_session/login/',
which allows the user to login for the first time,
and creates a new session for the user.
"""
import os
from typing import List, Tuple
import flask
from flask import request, jsonify, make_response
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """
    Handles session-based login
    """
    from api.v1.app import auth
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users_with_email: List[User] = User.search({"email": email})

    if not users_with_email:
        return jsonify({"error": "no user found for this email"}), 404

    user = users_with_email[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)

    session_cookie = os.environ.get("SESSION_NAME", "session_id")

    response = make_response(jsonify(user.to_json()))
    response.set_cookie(session_cookie, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=["DELETE"],
                 strict_slashes=False)
def logout() -> Tuple[flask.Response, int]:
    """
    docstring
    """
    from api.v1.app import auth

    assert isinstance(auth, SessionAuth)

    del_session = auth.destroy_session(flask.request)

    if del_session:
        return flask.jsonify(True), 200
    else:
        return flask.jsonify(False), 404
