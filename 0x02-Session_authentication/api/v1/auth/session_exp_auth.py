#!/usr/bin/env python3
"""Expiration date to a Session ID"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session expiration class"""
    def __init__(self):
        """Initialize the class"""
        super().__init__()
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create sessional function"""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Get user session id"""
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id)
        if not session_info:
            return None

        if self.session_duration <= 0:
            return session_info.get("user_id")

        created_at = session_info.get("created_at")
        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_info.get("user_id")
