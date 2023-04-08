from fastapi import FastAPI

app = FastAPI()


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