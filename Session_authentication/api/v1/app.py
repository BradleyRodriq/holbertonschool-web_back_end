#!/usr/bin/env python3
"""
Main file for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from models.user import User

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth: Auth = None

AUTH_TYPE: str = os.environ.get("AUTH_TYPE", None)

auth: Auth = None

if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def authenticate() -> None:
    """
    Authenticates the request
    """
    if auth is None:
        return

    if not auth.require_auth(
        request.path,
        ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/',
         '/api/v1/auth_session/login/']
    ):
        return

    auth_header: str = auth.authorization_header(request)
    session_cookie = auth.session_cookie(request)

    if auth_header is None and session_cookie is None:
        abort(401)

    user: User = auth.current_user(auth_header)

    if user is None:
        abort(403)

    request.current_user = user


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized (401) error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def unauthorized(error) -> str:
    """
    Forbidden (403) error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
