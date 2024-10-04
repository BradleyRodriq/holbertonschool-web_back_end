#!/usr/bin/env python3
"""
encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    _summary_
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
