#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """Database class defining
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """Add a new user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on the provided arguments"""
        if kwargs is None:
            raise InvalidRequestError
        for k in kwargs.keys():
            if not hasattr(User, k):
                raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound
        except InvalidRequestError as e:
            self._session.rollback()
            raise e
        except NoResultFound as e:
            self._session.rollback()
            raise e
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database based on the provided arguments"""
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError

        self._session.commit()
