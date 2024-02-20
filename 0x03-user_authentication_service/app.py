#!/usr/bin/env python3
"""Setting up basic flask app"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
