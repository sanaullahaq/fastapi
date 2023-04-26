from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#                         postgresql://<username>:<password>@<ip-address/hostname>/<database-name>
SQLALHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost/fastapi'
engine = create_engine(SQLALHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()