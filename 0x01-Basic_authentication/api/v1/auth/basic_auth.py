#!/usr/bin/env python3
"""Class BasicAuth  that inherits from Auth""" 
import base64
from api.v1.auth.auth import Auth


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
