from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh_token'
)
settings = Settings()


def create_token(data: dict) -> str:
    """Gera um token JWT

    Args:
        data (dict): claims do token

    Returns:
        str: token
    """
    expire = datetime.now(ZoneInfo('UTC')) + timedelta(
        minutes=settings.EXPIRE_MINUTES
    )
    data.update({'exp': expire})
    return encode(data, settings.SECRET_KEY_JWT, algorithm=settings.ALGORITHM)


def get_password_hash(password: str) -> str:
    """Converte uma senha em hash

    Args:
        password (str): senha do usuário

    Returns:
        str: hash da senha
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta

    Args:
        plain_password (str): senha limpa
        hashed_password (str): senha criptografada

    Returns:
        bool: se a senha está correta
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    """Obtém o usuário atual a partir do token JWT

    Args:
        token (str): token JWT

    Returns:
        User: usuário
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.SECRET_KEY_JWT, algorithms=[settings.ALGORITHM]
        )
        email = payload.get('sub')
        if not email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = await session.scalar(select(User).where(User.email == email))
    if not user:
        raise credentials_exception

    return user
