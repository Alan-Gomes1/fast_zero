from http import HTTPStatus

from fast_zero.schemas import UserPublic

USER = {'id': 1, 'username': 'Jhon', 'email': 'jhon@email.com'}


def test_create_user(client):
    data = {**USER, 'password': '123456'}
    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == USER


def test_create_user_conflict(client, user):
    data = {
        'username': user.username,
        'email': user.email,
        'password': user.password
    }
    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'username or email already exists'}


def test_list_users(client, user):
    users = [{'id': user.id, 'username': user.username, 'email': user.email}]
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': users}


def test_get_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_not_found(client):
    response = client.get('/users/2/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    data = {
        'username': 'Bob',
        'email': 'bob@email.com',
        'password': 'MyNewPassword',
    }
    response = client.put(
        f'/users/{user.id}/', headers={'Authorization': token}, json=data
    )
    del data['password']
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {**data, 'id': user.id}


def test_update_user_without_permissions(client, user, another_user, token):
    data = {
        'username': user.username,
        'email': user.email,
        'password': '645321',
    }
    url = f'/users/{another_user.id}/'
    response = client.put(url, headers={'Authorization': token}, json=data)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_conflict(client, user, another_user, token):
    new_user = {
        'username': another_user.username,
        'email': another_user.email,
        'password': '123456',
    }
    response = client.put(
        f'/users/{user.id}/', headers={'Authorization': token}, json=new_user
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'username or email already exists'}


def test_update_user_with_wrong_user(client, another_user, token):
    response = client.put(
        f'/users/{another_user.id}/',
        headers={'Authorization': token},  # o token está associado ao user
        json={
            'username': 'Bob', 'email': 'bob@email.com', 'password': '123456'
        }
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}/',
        headers={'Authorization': token},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_without_permissions(client, token):
    response = client.delete('/users/2/', headers={'Authorization': token})
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_with_wrong_user(client, another_user, token):
    response = client.delete(
        f'/users/{another_user.id}/', headers={'Authorization': token}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
