from http import HTTPStatus

import factory.fuzzy
import pytest

from fast_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text', max_nb_chars=30)
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': token},
        json={
            'title': 'Test Todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


@pytest.mark.asyncio
async def test_list_todos_shold_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get('/todos/', headers={'Authorization': token})

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': token},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_by_title(session, client, user, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Teste todo')
    )
    await session.commit()

    response = client.get(
        '/todos/?title=Teste todo',
        headers={'Authorization': token},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_by_description(session, client, user, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            5, user_id=user.id, description='Teste description'
        )
    )
    await session.commit()

    response = client.get(
        '/todos/?description=Teste description',
        headers={'Authorization': token},
    )

    assert len(response.json()['todos']) == expected_todos
