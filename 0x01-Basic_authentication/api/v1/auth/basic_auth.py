#!/usr/bin/env python3
"""Class BasicAuth  that inherits from Auth"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Creates class BasicAuth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Decodes base64 string"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        base64_credentials = authorization_header.split(" ", 1)[1]

        return base64_credentials

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Check if base64_authorization_header is None"""
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_bytes.decode('utf-8', errors='strict')
            return decoded_value
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Check if decoded_base64_authorization_header is None"""
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = (decoded_base64_authorization_header.split
                                     (':', 1))
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Check if user_email is None or not a string"""
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None

            if len(users) <= 0:
                return None

            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the authorization header from the request"""
        authorization_header = self.authorization_header(request)

        decoded_value = self.decode_base64_authorization_header(
            self.extract_base64_authorization_header(authorization_header)
        )

        user_email, user_password = (self.extract_user_credentials
                                     (decoded_value))

        user_instance = self.user_object_from_credentials(user_email,
                                                          user_password)

        return user_instance
