#!/usr/bin/env python3
""" authentication module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth"""
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path in excluded_paths:
            return False

        if not path.endswith('/'):
            path += '/'

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user"""
        return None
