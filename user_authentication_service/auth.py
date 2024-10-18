#!/usr/bin/env python3
"""
auth
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    hash password using bcrypt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
