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

    def get_user_from_session_id(self, session_id: str) -> Optional[str]:
        """ get user from session id """
        try:
            result: User = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return result

    def destroy_session(self, user_id: int) -> None:
        """
        destroy the session of the user
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        get reset token
        """
        try:
            user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email={email} doesn't exist.")

        reset_token: str = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update pw
        """
        try:
            user: User = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError(f"Invalid password reset token: {reset_token}")

        hashed_pw: str = _hash_password(password)

        try:
            self._db.update_user(
                user.id, reset_token=None, hashed_password=hashed_pw
            )
        except (NoResultFound, ValueError, Exception):
            raise
