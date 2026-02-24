def test_root_redirects_to_static_index(client):
    # Arrange: none
    # Act
    resp = client.get("/", allow_redirects=False)

    # Assert
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location") == "/static/index.html"
