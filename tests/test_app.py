from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_returns_200_ok():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello world'}


def test_content_page_hello():
    client = TestClient(app)
    response = client.get('/hello')
    assert 'Hello World' in response.text
