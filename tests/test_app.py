from http import HTTPStatus


def test_read_root_returns_200_ok(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello world'}


def test_content_page_hello(client):
    response = client.get('/hello')
    assert 'Hello World' in response.text


def test_create_user(client):
    data = {
        'username': 'test1',
        'email': 'test@email.com',
        'password': 'secret',
    }
    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test1',
        'email': 'test@email.com',
    }


def test_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'test1', 'email': 'test@email.com'}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'test2',
            'email': 'test2@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test2',
        'email': 'test2@example.com',
        'id': 1,
    }


def test_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'id': 2,
            'username': 'teste3',
            'password': 'secret',
            'email': 'teste@email.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
