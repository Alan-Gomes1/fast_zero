from fastapi import FastAPI

from .routers import auth, todos, users
from .schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)


@app.get('/')
async def read_root() -> Message:
    return {'message': 'Hello World'}
