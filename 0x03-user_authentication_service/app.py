#!/usr/bin/env python3
"""Setting up basic flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """Basic flask app setup"""
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"])
def register_user():
    """Check users existence and register if not"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(email, password)

        response_data = {"email": user.email, "message": "user created"}
        return jsonify(response_data), 200

    except ValueError as e:
        response_data = {"message": str(e)}
        return jsonify(response_data), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Get email and password from the request form data"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Retrieve session ID from the cookie"""
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def get_profile():
    """Get the user profile from cookie"""
    user_session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_session_id)
    if user_session_id is None or user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def reset_password_token():
    """Generates a password reset token for a user"""
    try:
        email = request.form['email']
        try:
            token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": token}), 200
        except ValueError:
            abort(403)
    except KeyError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """User's password update"""
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
    except KeyError:
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
