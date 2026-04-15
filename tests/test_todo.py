from http import HTTPStatus


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': token},
        json={
            'title': 'Test Todo',
            'description': 'Test todo description',
            'state': 'draft'
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test todo description',
        'state': 'draft',
    }
