from http import HTTPStatus

from fast_zero.settings import Settings

PASSWORD = Settings().FAKE_PASSWORD


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
