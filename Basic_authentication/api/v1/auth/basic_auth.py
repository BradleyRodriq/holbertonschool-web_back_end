#!/usr/bin/env python3
"""
Contains 'BasicAuth', which is an empty
child class of 'Auth'.
"""
import base64
from typing import Tuple, Optional
import binascii
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
        head = "Basic "

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith(head):
            return None

        return authorization_header[len(head):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Decodes the Base64 Authorization
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            return base64.b64decode(base64_authorization_header).decode()
        except (binascii.Error, ValueError, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts the user credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        return tuple(
            decoded_base64_authorization_header.split(':')
        )

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> Optional[User]:
        """
        Returns the User object
        """

        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            for user in User.all():
                if user.email == user_email and \
                        user.is_valid_password(user_pwd):
                    return user
        except KeyError:
            pass

        return None

    def current_user(self, request=None) -> Optional[User]:
        """
        Returns the User object
        """
        base_64_auth_header = self.extract_base64_authorization_header(
            request
        )

        auth_header = self.decode_base64_authorization_header(
            base_64_auth_header
        )


        user_credentials = self.extract_user_credentials(
            auth_header
        )

        result = self.user_object_from_credentials(*user_credentials)

        return result
