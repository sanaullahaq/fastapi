from app.schemas import *
from .test_db_conn import client, session
# though we are not using session directly here,
# but since client is depended on session so we need to import session as well


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World!!!'
    assert res.status_code == 200  # default status_code in FastAPI is 200


"""
only passing `/users` here will cause issue in the case of testing.
in the browser if we send request to `/users` only, FastAPI is as smart as it redirects the requests to `/users/`.
with status code 307. and after redirect, finallty we got status code 201

but while in the test we captured the status code 307 if we just request to url `/users` rather `/users/`.
and it causes test failed. so need to be specific here regarding testing
----------------------------------------------------------------------------------
| now a days pytest is also as smart as FastAPI, it tooks the final status code, |
| not the status code where it is redirected from.                               |
----------------------------------------------------------------------------------
"""
def test_create_user(client):
    res = client.post(
        # passing request body-json data with `json`
        "/users/", json={"email": "test1@gmail.com", "password": "12345"})
    # print(res.json())
    new_user = UserOut(**res.json())
    assert new_user.email == "test1@gmail.com"
    assert res.status_code == 201
    # print(res.status_code)

def test_login(client):
    res = client.post(
        # passing request body-json data with `json`
        "/users/", json={"email": "test1@gmail.com", "password": "12345"})
    # passing request body-form data with `data`
    res = client.post("/login", data={"username": "test1@gmail.com", "password": "12345"})
    print(res.json())
    assert res.status_code == 200