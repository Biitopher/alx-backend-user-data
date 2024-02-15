#!/usr/bin/env python3
"""Class SessionAuth that inherits from Auth"""
from api.v1.auth.auth import Auth
import uuid
from flask import Flask, request, jsonify
from api.v1.views import app
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        if request is None:
            return None

        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    @app.route('/auth_session/login', methods=['POST'])
    def session_login():
        """Session authentication"""
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400

        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search({'email': email})

        if not user:
            return jsonify({"error": "no user found for this email"}), 404

        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = auth.create_session(user.id)
        response_data = user.to_json()

        session_cookie_name = app.config.get('SESSION_NAME', 'session_id')
        response = jsonify(response_data)
        response.set_cookie(session_cookie_name, session_id)

        return response
