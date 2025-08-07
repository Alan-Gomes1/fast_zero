from http import HTTPStatus

from freezegun import freeze_time

from fast_zero.settings import Settings

PASSWORD = Settings().FAKE_PASSWORD
EXPIRE_MINUTES = Settings().EXPIRE_MINUTES


def test_get_token(client, user):
    response = client.post(
        'auth/token', data={'username': user.email, 'password': PASSWORD}
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_login_with_invalid_email(client, user):
    data = {'username': 'invalid@email.com', 'password': PASSWORD}
    response = client.post('auth/token', data=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}


def test_login_with_invalid_password(client, user):
    data = {'username': user.email, 'password': 'wrongpassword'}
    response = client.post('auth/token', data=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}


def test_token_expired_after_time(client, user, token):
    with freeze_time('2026-01-01 12:00:00'):
        data = {'username': user.email, 'password': PASSWORD}
        response = client.post('auth/token', data=data)
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time(f'2026-01-01 12:{EXPIRE_MINUTES + 1}:00'):
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'username': 'Bob',
            'email': 'bob@email.com',
            'password': 'MyNewPassword'
        }
        response = client.put(f'/users/{user.id}/', headers=headers, json=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, token):
    response = client.post(
        'auth/refresh_token', headers={'Authorization': token}
    )
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'Bearer'
