from typing import Optional
from pydantic import BaseModel
#both Body class works same (findings till now)
# from fastapi import Body
from fastapi.params import Body
from fastapi import FastAPI



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # If the user does not provide published value the default will be True
    rating: Optional[int] = None #  Optional with default None




@app.get("/")
def root():
    return {"message": "Hello World, this is my api"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    posts = [
        {
        'id': 1,
        'text': 'text id 1'
        },
        {
        'id': 2,
        'text': 'text id 2'
        },
        {
        'id': 3,
        'text': 'text id 3'
        }
    ]
    for post in posts:
        if post['id'] == post_id:
            return {'text': post['text']}

"""
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    '''
    the Body class will convert the HTTP request Body into a dict and store in payload parameter.
    '''
    print(payload)
    return {"message": f"title: {payload['title']} content: {payload['content']}"}
"""

#it is very painful to extract data from HTTP Body, what we can do is given below
@app.post("/createposts")
def create_posts(post: Post):
    '''
    the pydantic (schema model) Post class will validate the data sent by user via HTTP Body.
    It will look for the defined attributes and defined type attributes
    if it finds everything okk then the data will be stored in post else
    error will be thrown
    '''
    print(post) # printing pydantic model 
    print(post.dict()) # converted into regular dict using dict() method of pydantic model
    return {"data": post.dict()}