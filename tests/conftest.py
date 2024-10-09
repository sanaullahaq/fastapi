"""
`conftest.py` is a pytest specific configuration file.
we can put all our fixtures here and we do not need to import those fixture to use.
pytest will automatically look for those fixture into the `conftest.py` file.
**`conftest.py` file must be inside the `tests` package.**
All the subpackage(if we define) can also access this `conftest.py`

however if we want we can define a separate `conftest.py` inside the subpackage of package `tests`.
Then subpackage will use that `conftest.py`. and the upper level test modules/files will not have accesss to the `conftest.py` file
inside the subpackage
"""


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.database import get_db, Base
from app.main import app
from app.config import settings
from sqlalchemy.orm import sessionmaker
import pytest

from app.oauth2 import create_access_token

# fastapi_test DB for testing purpose
SQLALHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{
    settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture(scope='module')
@pytest.fixture
def session():
    # here, we have imported `Base` object directly from the `app.database`,
    # thats why we do not need to put `models.Base...` as in the main.py file
    Base.metadata.drop_all(bind=engine)     # clean the DB
    Base.metadata.create_all(bind=engine)   # fresh DB
    # idea behind the cleaning the DB first and then creating the fresh DB is that,
    # when a test will be failed we can look into the DB state/situation and analyse
    # and on the completion of the test, DB will be remained.

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# fixture depended on fixture
# @pytest.fixture(scope='module')
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    """
    We have created a Test DB for testing purpose and we are overriding the actual `get_db` depency of our `app` with `override_get_db`
    So that all our testing purpose related queries runs into the test DB
    """
    app.dependency_overrides[get_db] = override_get_db

    # `yield` operator will return the value it generates, it can generate multiple values and send them as list
    # most important `yield` will let execute the function till the end where it will also send the generated value(s) as well
    # unlike `return`, `return` statement stops the execution of the function after retuern statement
    yield TestClient(app)
    # Base.metadata.drop_all(bind=engine)       # this will clean the DB, and we will not able to analyse DB state if any test fails

@pytest.fixture
def test_user(client):
    user_data = {"email": "sanau@xyz.com", "password": "12345"}
    # passing request body-json data with `json`
    res = client.post("/users/", json=user_data)
    assert res.status_code==201
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


# creating token with user id, what is same as what token we get back after login.
# and then authorizing the client with token.
# sending the token data in the header of the request.
@pytest.fixture
def authorized_client(client, token):
    print(f"client.headers: {client.headers}")
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    print(f"client.headers: {client.headers}")
    return client