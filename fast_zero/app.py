from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello world'}


@app.get('/hello', response_class=HTMLResponse)
def hello():
    return """
        <html><body>
            <h2>Hello World</h2>
        <body><html>
    """
