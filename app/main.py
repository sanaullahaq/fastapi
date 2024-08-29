from . database import engine
from . import models
from fastapi import FastAPI
from . routers import posts, users, auth
from . config import settings

print(settings.path)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(posts.router)
# this includes the path-operations lives in 'routers/posts.py' file using object 'router' of type 'APIRouter'

app.include_router(users.router)
# this includes the path-operations lives in 'routers/users.py' file using object 'router' of type 'APIRouter'

app.include_router(auth.router)

@app.get("/")
def root():
	return {"message": "Hello World, this is my api"}