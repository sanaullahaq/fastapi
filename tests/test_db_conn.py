from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.database import get_db, Base
from app.main import app
from app.config import settings
from sqlalchemy.orm import sessionmaker
import pytest

# fastapi_test DB for testing purpose
SQLALHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{
    settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='module')
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
@pytest.fixture(scope='module')
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