#!/usr/bin/env python3
"""Sessions in database"""
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    def create_session(self, user_id=None):
        """Create session function"""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Get user session id"""
        if session_id is None:
            return None

        user_session = UserSession.load_from_file(session_id)
        if not user_session:
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy the session"""
        if request is None:
            return

        session_id = SessionDBAuth().session_cookie(request)
        if session_id:
            user_session = UserSession.load_from_file(session_id)
            if user_session:
                user_session.delete()
