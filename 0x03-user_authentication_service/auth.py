#!/usr/bin/env python3
"""Define hash password method"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password with salt using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes the instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Try locating the user validity by email"""
        try:
            user = self._db.find_user_by(email=email)

            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create user session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid.uuid4())
            self._db.update_user_session_id(user.id, session_id)
            return session_id

        except NoResultFound:
            return None
