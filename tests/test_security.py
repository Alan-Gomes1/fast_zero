from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_token
from fast_zero.settings import Settings

SECRET_KEY_JWT = Settings().SECRET_KEY_JWT


def test_jwt():
    data = {'test': 'test'}
    token = create_token(data)
    decoded = decode(token, SECRET_KEY_JWT, algorithms=['HS256'])
    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_invalid_email(client):
    token = create_token({'sub': 'invalid@email.com'})
    response = client.put(
        '/users/1/',
        headers={'Authorization': f'Bearer {token}'}, json={'email': 'invalid'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_without_email(client):
    token = create_token({'test': 'test'})  # No 'sub' in payload
    response = client.put(
        '/users/1/', headers={'Authorization': f'Bearer {token}'}, json={}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
