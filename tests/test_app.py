from http import HTTPStatus

from fast_zero.settings import Settings

USER = {'id': 1, 'username': 'Jhon', 'email': 'jhon@email.com'}
PASSWORD = Settings().FAKE_PASSWORD


def test_read_root_shold_return_200_ok(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
