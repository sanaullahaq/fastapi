from . database import engine
from . import models
from fastapi import FastAPI
from . routers import posts, users, auth, votes
from . config import settings
from fastapi.middleware.cors import CORSMiddleware

"""
At the start-up of the program we are commanding `sqlalchemy` to create all the tables,
Since at the current stage of the program we are usig `alembic` database migrations tool,
We dont need this command,
However we can keep this command, subject to `alembics` first revision will not going to do anything,
As everything is already there.
"""
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
# origins = [
#     "https://google.com",
#     "https://youtube.com",
# ]
origins=["*"]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)
"""
Basically we are allowing everybody(origins) to send API request to our server with `origins=["*"]`
`allow_credentials=True` -> Credentials (Authorization headers, Cookies, etc).
`allow_methods=["*"]` -> Specific HTTP methods (POST, PUT) or all of them with the wildcard "*".
`allow_headers=["*"]` -> Specific HTTP headers or all of them with the wildcard "*".

CORS - Cross-Origin Resource Sharing: comes handy when you server is made for private use, only
request from specific origins will be allowed, only specific methods will be allowed. etc etc.
"""

app.include_router(posts.router)
# this includes the path-operations lives in 'routers/posts.py' file using object 'router' of type 'APIRouter'

app.include_router(users.router)
# this includes the path-operations lives in 'routers/users.py' file using object 'router' of type 'APIRouter'

app.include_router(auth.router)

app.include_router(votes.router)

@app.get("/")
def root():
	return {"message": "Hello World!!! This is Sanaulla"}