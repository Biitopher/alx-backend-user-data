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
def login() -> str:
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
def logout() -> None:
    """Retrieve session ID from the cookie"""
    user = None
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
