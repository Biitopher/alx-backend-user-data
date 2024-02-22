#!/usr/bin/env python3
"""Define hash password method"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password with salt using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate new UUID"""
    return str(uuid.uuid4())


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
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Check if the session_id is None"""
        if not session_id:
            return None
        try:
            user = self._db.get_user_by_session_id(session_id=session_id)

            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Use public method to update the corresponding user's session ID"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user_session_id(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Password reset token generation """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(cls, reset_token, new_password):
        """Find the user with the given reset_token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError