#!/usr/bin/env python3
"""DB module
"""
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        creates a new user object
        """
        new_user: User = User(
            email=email,
            hashed_password=hashed_password,
        )

        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        returns the first row found on the users table
        """
        found_user: Union[User, None] = self._session.query(User) \
            .filter_by(**kwargs) \
            .first()

        if found_user is None:
            raise NoResultFound

        return found_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        updates user
        """
        user: User = self.find_user_by(id=user_id)

        if 'id' in kwargs:
            raise ValueError("Cannot update 'id' of 'User'.")

        for attr, value in kwargs.items():
            if attr not in user.__dict__.keys():
                raise ValueError(f"'User' object has no attribute '{attr}'")
            setattr(user, attr, value)
