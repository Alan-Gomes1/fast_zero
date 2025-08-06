from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='Jhon', password='123456', email='jhon@email.com'
        )
        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'Jhon')
        )

        assert asdict(user) == {
            'id': 1,
            'username': 'Jhon',
            'password': '123456',
            'email': 'jhon@email.com',
            'create_at': time,
            'updated_at': time,
        }
