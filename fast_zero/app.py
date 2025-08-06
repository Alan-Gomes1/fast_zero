from fastapi import FastAPI

from .routers import auth, users
from .schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get('/')
async def read_root() -> Message:
    return {'message': 'Hello World'}
