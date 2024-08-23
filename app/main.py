from . database import engine
from . import models
import time
from psycopg2.extras import RealDictCursor
import psycopg2
from fastapi import FastAPI
from . routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
	try:
		"""
		Psycopg – PostgreSQL database adapter for Python,
		But psycopg does not return the column name, so to get the column name we set 'cursor_factory=RealDictCursor'
		"""
		conn = psycopg2.connect(host='localhost',
								database='fastapi',
								user='postgres',
								password='12345',
								cursor_factory=RealDictCursor)
		cursor = conn.cursor()
		print('***---***Database connection was successful***---***')
		break
	except Exception as error:
		print('Connecting to Database failed!')
		print('Error: ', error)
		time.sleep(5)			#try again after 5 seconds

# def find_post(id):
#     for post in my_posts:
#         if post['id'] == id:
#             return post

# def find_index_post(id):
#     for i, post in enumerate(my_posts):
#         if post['id'] == id:
#             return i

# this includes the path-operations lives in 'routers/posts.py' file using object 'router' of type 'APIRouter'
app.include_router(posts.router)
# this includes the path-operations lives in 'routers/users.py' file using object 'router' of type 'APIRouter'
app.include_router(users.router)

app.include_router(auth.router)

@app.get("/")
def root():
	return {"message": "Hello World, this is my api"}