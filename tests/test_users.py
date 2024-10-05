from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.database import get_db, Base
from app.main import app
from app.schemas import *
from app.config import settings
from sqlalchemy.orm import sessionmaker

# fastapi_test DB for testing purpose
SQLALHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{
    settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# here, we have imported `Base` object directly from the `app.database`,
# thats why we do not need to put `models.Base...` as in the main.py file
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
We have created a Test DB for testing purpose and we are overriding the actual `get_db` depency of our `app` with `override_get_db`
So that all our testing purpose related queries runs into the test DB
"""
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World!!!'
    assert res.status_code == 200  # default status_code in FastAPI is 200


def test_create_user():
    res = client.post(
        # passing request body as json data
        "/users/", json={"email": "test1@gmail.com", "password": "12345"})
    print(res.json())
    new_user = UserOut(**res.json())
    assert new_user.email == "test1@gmail.com"
    assert res.status_code == 201
