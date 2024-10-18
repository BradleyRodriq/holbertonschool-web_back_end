#!/usr/bin/env python3
"""
auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    hash password using bcrypt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


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
