from http import HTTPStatus
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import FilterTodo, TodoList, TodoPublic, TodoSchema
from fast_zero.security import get_current_user

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema, user: CurrentUser, session: Session
) -> Todo:
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    return new_todo


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
async def list_todos(
    user: CurrentUser,
    session: Session,
    todo_filter: Annotated[FilterTodo, Query()],
) -> dict[str, Sequence[Todo]]:
    query = select(Todo).where(Todo.user_id == user.id)
    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(
        query.offset(todo_filter.skip).limit(todo_filter.limit)
    )

    return {'todos': todos.all()}
