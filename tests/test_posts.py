def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts/")
    print(res.json())