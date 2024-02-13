#!/usr/bin/env python3
"""API authentication class"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Validates if a request needs authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Retrieves the Authorization header from the request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from the request"""
        return None
