#!/usr/bin/env python3
""" auth """
from typing import Union
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """_summary_

    Args:
        Auth (_type_): _description_
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """_summary_

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id: str = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        docstring
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> Union[User, None]:
        """
        docstring
        """

        if request is None:
            return None

        cookie = self.session_cookie(request)

        uid = self.user_id_for_session_id(cookie)

        user = User.get(uid)
        return user

    def destroy_session(self, request=None) -> bool:
        """
        docstring
        """
        if request is None:
            return False

        session_id: str = self.session_cookie(request)

        if session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
