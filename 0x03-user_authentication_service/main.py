#!/usr/bin/env python3
""" End-to-end integration test"""
import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """register the user"""
    url = f"{BASE_URL}/register"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Error log in wrong password"""
    url = f"{BASE_URL}/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in email with password"""
    url = f"{BASE_URL}/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    return response.json()["session_id"]


def profile_unlogged() -> None:
    """Unlog the  profile logged on"""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 401


def profile_logged(session_id: str) -> None:
    """Log on the profile"""
    url = f"{BASE_URL}/profile"
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """End session by log out"""
    url = f"{BASE_URL}/logout"
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """ Reset the password token"""
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the current password"""
    url = f"{BASE_URL}/update_password"
    payload = ({"email": email,
               "reset_token": reset_token, "new_password": new_password})
    response = requests.post(url, json=payload)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
