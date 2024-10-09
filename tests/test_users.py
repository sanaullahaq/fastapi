from jose import jwt
from app.config import settings
import pytest
from app import schemas
# from .test_db_conn import client, session
# though we are not using session directly here,
# but since client is depended on session so we need to import session as well


# @pytest.fixture
# def test_user(client):
#     user_data = {"email": "sanau@xyz.com", "password": "12345"}
#     # passing request body-json data with `json`
#     res = client.post("/users/", json=user_data)
#     assert res.status_code==201
#     # print(res.json())
#     new_user = res.json()
#     new_user["password"] = user_data["password"]
#     return new_user


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World!!!'
#     assert res.status_code == 200  # default status_code in FastAPI is 200


"""
only passing `/users` here will cause issue in the case of testing.
in the browser if we send request to `/users` only, FastAPI is as smart as it redirects the requests to `/users/`.
with status code 307. and after redirect, finallty we got status code 201

but while in the test we captured the status code 307 if we just request to url `/users` rather `/users/`.
and it causes test failed. so need to be specific here regarding testing
----------------------------------------------------------------------------------
| now a days pytest is also as smart as FastAPI, it tooks the final status code, |
| not the status code from where it is has been redirected .                     |
----------------------------------------------------------------------------------
"""
def test_create_user(client):
    res = client.post(
        # passing request body-json data with `json`
        "/users/", json={"email": "test1@gmail.com", "password": "12345"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test1@gmail.com"
    assert res.status_code == 201
    # print(res.status_code)


"""
created user in the above `test_create_user()` method will not be existed while running the below `test_login()` method,
so test_login() will be failed. we can approach 3ways.
1- we can use scope inside the fixture. EX: @pytest.fixture(scope='module').
    So a fixture will be ran only once based on each module(in our case test_xxx.py file).
    Deafault value of the `scope='function'`. So by default it ran everytime a test function called.
    But using fixture with scope='module' will make the `test_login()` depended on `test_create_user()` or if you put `test_login`
    above `test_create_user()` also the test will be failed.
    So in summary this is not a good practice. A test case should not depended on another test case.
    More about fixture: https://docs.pytest.org/en/6.2.x/fixture.html#:~:text=requesting%20it%0A%20%20%20%20...-,Fixture%20scopes%C2%B6,-Fixtures%20are%20created
2- explicitly create an user inside test_login() and apply `login` on that user. This is a better approach then explained in step 1
3- *most convenient approach*
    We will define another fixture what will return a test user. And we will try to login with the test user.
    We will use this fixture whenever we need a test user.
"""
def test_login_user(test_user, client):
    # res = client.post("/users/", json={"email": "test1@gmail.com", "password": "12345"})
    # passing request body-form data with `data`
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    assert test_user['id'] == payload.get('user_id')
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200



@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@xyz.com", "12345", 403),
    ("test1@gmail.com", "wrongpassword", 403),
    ("wrongemail@xyz.com", "wrongpassword", 403),
    (None, "12345", 422),
    ("test1@gmail.com", None, 422)
])
# status_code 422 - > schema validation error
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json()["detail"] == "Invalid Credentials"