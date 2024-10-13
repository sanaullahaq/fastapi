from app.schemas import PostOut, Post
import pytest
from app import models
from tests.conftest import test_posts

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return PostOut(**post)
    posts_list = list(map(validate, res.json()))

    assert res.status_code == 200
    # print(len(res.json()))
    assert len(res.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    # print(res.status_code)
    assert res.status_code ==  401


def test_unathoraized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    # print(res.status_code)
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/111")
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    for idx in range(len(test_posts)):
        res = authorized_client.get(f"/posts/{test_posts[idx].id}")
        post = PostOut(**res.json())

        # print(idx)
        # print(res.status_code)
        # print(res.json())

        assert post.Post.id == test_posts[idx].id
        assert post.Post.title == test_posts[idx].title
        assert post.Post.content == test_posts[idx].content


@pytest.mark.parametrize("title, content, published",[
    ("new title 1", "new content 1", False),
    ("new title 2", "new content 2", True),
    ("new title 3", "new content 3", False)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    # print(res.status_code)
    # print(res.json())
    created_post = Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.id == test_user['id']


@pytest.mark.parametrize("title, content", [
    ("new title 1", "new content 1"),
    ("new title 2", "new content 2"),
    ("new title 3", "new content 3")
])
def test_create_post_default_published_true(authorized_client, test_user, title, content,):
    res = authorized_client.post("/posts/", json={"title": title, "content": content})
    # print(res.status_code)
    # print(res.json())
    created_post = Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True
    assert created_post.id == test_user['id']


def test_unathoraized_user_create_post(client):
    res = client.post("/posts/", json={"title": "test title", "content": "test_content"})
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 401


def test_unathoraized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    # print(res.status_code)
    res.status_code == 204
    # if res.status_code == 204:
    #     print("No Content")
    # print(res.json()) # will throw error
    # The HTTP status code 204 No Content indicates that the server successfully processed the request, but there is no content to return in the response body. When you try to call res.json() on a 204 No Content response, it will raise an error because there is no JSON content to parse.


def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete(f"/posts/111")
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    # test_posts[1] belongs to test_user2, but authoraized_client comes from test_user
    res = authorized_client.delete(f"/posts/{test_posts[1].id}")
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    # print(res.status_code)
    # print(res.json())

    post = Post(**res.json())
    assert post.title == data["title"]
    assert post.content == data["content"]
    assert post.id == data["id"]


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[1].id
    }
    res = authorized_client.put(f"/posts/{test_posts[1].id}", json=data)
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/111", json=data)
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 404