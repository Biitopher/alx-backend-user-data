#!/usr/bin/env python3
"""Handle User session storage"""
from models.base import Base


class UserSession(Base):
    """The class user session"""
    def __init__(self, *args, user_id=None, session_id=None, **kwargs):
        """Initialize the session"""
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.session_id = session_id
