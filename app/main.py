from random import randrange
from typing import Optional
from pydantic import BaseModel
# both Body class works same (findings till now)
# from fastapi import Body
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    # If the user does not provide published value the default will be True
    published: bool = True
    rating: Optional[int] = None  # Optional with default None


my_posts = [
    {
        'id': 1,
        'title': 'title of post 1',
        'content': 'content of post 1'
    },
    {
        'id': 2,
        'title': 'my favorite foods',
        'content': 'i love pizza'
    }
]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World, this is my api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# when there could be multiple type of status
@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'Post with id {d} was not found'}
    return {'data': post}


"""
@app.post("/posts")
def create_posts(payload: dict = Body(...)):
    '''
    the Body class will convert the HTTP request Body into a dict and store in payload parameter.
    '''
    print(payload)
    return {"message": f"title: {payload['title']} content: {payload['content']}"}
"""

# it is very painful to extract data from HTTP Body, what we can do is given below


# when there is only one success status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    '''
    the pydantic (schema model) Post class will validate the data sent by user via HTTP Body.
    It will look for the defined attributes and defined type attributes
    if it finds everything okk then the data will be stored in post else
    error will be thrown
    '''
    # print(post) # printing pydantic model
    # print(post.dict()) # converted into regular dict using dict() method of pydantic model
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    my_posts.pop(index)

    '''
    since this is a delete request that's why the status code is 204
    and when the status code is 204 the convention or fastapi does not want us to return any data but a response
    '''
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}

