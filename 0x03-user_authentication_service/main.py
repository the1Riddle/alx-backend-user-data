#!/usr/bin/env python3
"""
End-to-end integration test
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Integeration test for validating user registeration"""
    payload = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/users", data=payload)
    msg = {"email": email, "message": "user created"}

    assert res.status_code == 200
    assert res.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """Integeration test for validating login with wrong password"""
    payload = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/sessions", data=payload)

    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
        Test for validating user login with correct credentials
    """
    payload = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/sessions", data=payload)
    msg = {"email": email, "message": "logged in"}

    assert res.status_code == 200
    assert res.json() == msg

    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test user's profile unlogged"""
    cookies = {"session_id": ""}
    res = requests.get(f"{BASE_URL}/profile", cookies=cookies)

    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Validate user's profile logged in"""
    cookies = {"session_id": session_id}
    res = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    msg = {"email": EMAIL}

    assert res.status_code == 200
    assert res.json() == msg


def log_out(session_id: str) -> None:
    """Validate log out route handler"""
    cookies = {"session_id": session_id}
    res = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    msg = {"message": "Bienvenue"}

    assert res.status_code == 200
    assert res.json() == msg


def reset_password_token(email: str) -> str:
    """Validate reset password token route handler"""
    payload = {"email": email}
    res = requests.post(f"{BASE_URL}/reset_password", data=payload)

    token = res.json().get("reset_token")
    msg = {"email": email, "reset_token": token}

    assert res.status_code == 200
    assert res.json() == msg

    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Validate update password route handler"""

    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
        }

    res = requests.put(f"{BASE_URL}/reset_password", data=payload)
    msg = {"email": email, "message": "Password updated"}

    assert res.status_code == 200
    assert res.json() == msg


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
