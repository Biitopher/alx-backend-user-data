#!/usr/bin/env python3
""" Module of Users views"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Session authentication login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    response_data = user[0].to_json()
    response = make_response(jsonify(response_data), 200)
    session_cookie_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_cookie_name, session_id)

    return response
