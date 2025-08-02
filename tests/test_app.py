from http import HTTPStatus

from fast_zero.schemas import UserPublic

USER = {'id': 1, 'username': 'Jhon', 'email': 'jhon@email.com'}


def test_read_root_shold_return_200_ok(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    data = {**USER, 'password': '123456'}
    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == USER


def test_create_user_conflict(client, user):
    data = {**USER, 'password': '123456'}
    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'username or email already exists'}


def test_list_users(client, user):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [USER]}


def test_get_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_not_found(client):
    response = client.get('/users/2/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    data = {
        'username': 'Bob',
        'email': 'bob@email.com',
        'password': 'MyNewPassword',
    }
    response = client.put('/users/1/', json=data)
    del data['password']
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {**data, 'id': 1}


def test_update_user_not_found(client):
    data = {
        'username': 'Doe',
        'email': 'doe@email.com',
        'password': '645321',
    }
    response = client.put('/users/2/', json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_conflict(client, user):
    new_user = {
        'username': 'Bob', 'email': 'bob@email.com', 'password': '123456'
    }
    client.post('/users/', json=new_user)
    response = client.put(f'/users/{user.id}/', json=new_user)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'username or email already exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1/')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client):
    response = client.delete('/users/1/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
