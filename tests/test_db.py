from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='jhon', password='secret', email='test@email.com'
    )
    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'test@email.com')
    )

    assert result.id == 1
    assert result.username == 'jhon'
