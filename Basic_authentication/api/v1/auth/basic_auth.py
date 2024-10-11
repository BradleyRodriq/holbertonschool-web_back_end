#!/usr/bin/env python3
"""
Contains 'BasicAuth', which is an empty
child class of 'Auth'.
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Child class of 'Auth'.
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """_summary_

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        HEADER_START = "Basic "

        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith(HEADER_START):
            return None

        return authorization_header[len(HEADER_START):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Decodes the Base64 Authorization
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        return tuple(
            decoded_base64_authorization_header.split(':')
        )

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Returns the User object
        """

        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None

        try:
            for user in User.all():
                if user.email == user_email and \
                        user.is_valid_password(user_pwd):
                    return user
        except KeyError as e:
            pass

        return None

    def current_user(self, request: str = None) -> TypeVar('User'):
        """
        Returns the User object
        """

        BASE_64_AUTH_HEADER = self.extract_base64_authorization_header(
            request
        )

        AUTH_HEADER = self.decode_base64_authorization_header(
            BASE_64_AUTH_HEADER
        )

        USER_CREDENTIALS = self.extract_user_credentials(
            AUTH_HEADER
        )

        RESULT = self.user_object_from_credentials(*USER_CREDENTIALS)

        return RESULT
