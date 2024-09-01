from . database import engine
from . import models
from fastapi import FastAPI
from . routers import posts, users, auth, votes
from . config import settings

"""
At the start-up of the program we are commanding `sqlalchemy` to create all the tables,
Since at the current stage of the program we are usig `alembic` database migrations tool,
We dont need this command, 
However we can keep this command, subject to `alembics` first revision will not going to do anything,
As everything is already there.
"""
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(posts.router)
# this includes the path-operations lives in 'routers/posts.py' file using object 'router' of type 'APIRouter'

app.include_router(users.router)
# this includes the path-operations lives in 'routers/users.py' file using object 'router' of type 'APIRouter'

app.include_router(auth.router)

app.include_router(votes.router)

@app.get("/")
def root():
	return {"message": "Hello World, this is my api"}