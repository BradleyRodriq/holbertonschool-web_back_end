#!/usr/bin/env python3
"""
auth
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    hash password using bcrypt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ returns uuid """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a new user
        """
        try:
            user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            hash_pw = _hash_password(password)
            return self._db.add_user(email, hash_pw)
        else:
            raise ValueError(f"User {email} already exists.")

    def valid_login(self, email: str, password: str) -> bool:
        """ checks if user info is valid """
        try:
            valid_user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(
                password.encode(),
                valid_user.hashed_password
            )

    def create_session(self, email: str) -> Optional[str]:
        """
        creates a session
        """
        try:
            user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user_session: str = _generate_uuid()
            self._db.update_user(user.id, session_id=user_session)
            return user_session
