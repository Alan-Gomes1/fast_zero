from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='Jhon', password='123456', email='jhon@email.com'
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'Jhon'))

        assert asdict(user) == {
            'id': 1,
            'username': 'Jhon',
            'password': '123456',
            'email': 'jhon@email.com',
            'create_at': time,
            'updated_at': time,
        }
