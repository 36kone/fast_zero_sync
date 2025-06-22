from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='kone', email='kone@email.com', password='senha_legal')

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'kone@email.com'))

    assert result.username == 'kone'
