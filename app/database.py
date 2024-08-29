from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . config import settings


#                           postgresql://<username>:<password>@<ip-address-OR-hostname:port>/<database-name>
# SQLALHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost:5432/fastapi'
SQLALHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()



"""
Psycopg – PostgreSQL database adapter for Python,
But psycopg does not return the column name, so to get the column name we set 'cursor_factory=RealDictCursor'
"""
# import time
# from psycopg2.extras import RealDictCursor
# import psycopg2
# while True:
# 	try:
# 		conn = psycopg2.connect(host='localhost',
# 								database='fastapi',
# 								user='postgres',
# 								password='12345',
# 								cursor_factory=RealDictCursor)
# 		cursor = conn.cursor()
# 		print("--------------------------------------\n| Database connection was successful |\n--------------------------------------")
# 		break
# 	except Exception as error:
# 		print('Connecting to Database failed!')
# 		print('Error: ', error)
# 		time.sleep(5)			#try again after 5 seconds