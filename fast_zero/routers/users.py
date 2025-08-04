from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import FilterPage, UserList, UserPublic, UserSchema
from fast_zero.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):
    query = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if query:
        error_message = 'username or email already exists'
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=error_message
        )
    new_user = User(**user.model_dump())
    new_user.password = get_password_hash(user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get('/', response_model=UserList)
def list_users(session: Session, filter: Annotated[FilterPage, Query()]):
    users = session.scalars(
        select(User).offset(filter.skip).limit(filter.limit)
    ).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session, current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        session.commit()
        session.refresh(current_user)
    except IntegrityError:
        error_message = 'username or email already exists'
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=error_message
        )
    return current_user


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    user_id: int, session: Session, current_user: CurrentUser,
) -> None:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    session.delete(current_user)
    session.commit()
