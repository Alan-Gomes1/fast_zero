from contextlib import contextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash
from fast_zero.settings import Settings

TZ_INFO = ZoneInfo('America/Sao_Paulo')
PASSWORD = Settings().FAKE_PASSWORD


@pytest.fixture
def client(session):
    """Cria um cliente de teste que utiliza uma sessão do banco de dados
    de teste. A sessão é passada como uma dependência para o app, permitindo
    que os testes interajam com o banco de dados em memória sem afetar o
    estado real do banco de dados. Após os testes, a dependência é limpa.

    Args:
        session (Session): Sessão do banco de dados para testes.

    Yields:
        TestClient: Cliente de teste configurado com a sessão do banco de dados

    Exemplo de uso:
        ```def test_example(client):
            response = client.get('/some-endpoint')
            assert response.status_code == 200
            assert response.json() == {'key': 'value'}
    """
    def get_session_override():
        """Função de substituição para a dependência get_session, que retorna
        a sessão de teste fornecida. Isso permite que o app use a sessão
        de teste em vez de criar uma nova sessão para cada requisição.

        Returns:
            Session: Sessão dos testes.
        """
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    """Cria uma sessão de banco de dados para testes utilizando um banco
    de dados SQLite em memória. A sessão é criada com um pool estático para
    evitar problemas de concorrência em testes que podem ser executados em
    paralelo. Após os testes, a tabela é removida do banco de dados.

    Yields:
        Session: Sessão do banco de dados para testes.
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    """Cria um usuário de teste no banco de dados.

    Args:
        session (Session): Sessão do banco de dados para testes.

    Yields:
        User: Usuário de teste criado.
    """
    password = get_password_hash(PASSWORD)
    user = User(username='Jhon', email='jhon@email.com', password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@contextmanager
def _mock_db_time(*, model, time=datetime.now(TZ_INFO).replace(tzinfo=None)):
    """Mocka o tempo de criação e atualização de um modelo no banco de dados.

    Isso é útil para garantir que os testes não dependam do tempo real e
    possam ser executados de forma determinística. O tempo pode ser
    personalizado passando o parâmetro `time`.

    Args:
        model (Object): Modelo do SQLAlchemy a ser mockado.
        time (datetime, optional): Tempo utilizado para os campos mockados
            Defaults to datetime.now(TZ_INFO).replace(tzinfo=None).

    Yields:
        datetime: Tempo mockado.
    """
    def fake_time_hook(mapper, connection, target):
        """Hook para definir o tempo de criação e atualização do modelo.
        Este hook é chamado antes de inserir o modelo no banco de dados,
        permitindo que os campos `create_at` e `updated_at` sejam definidos
        com o tempo mockado.

        Args:
            mapper: Mapeador do SQLAlchemy.
            connection: Conexão com o banco de dados.
            target: Instância do modelo a ser inserido.
        """
        if hasattr(target, 'create_at'):
            target.create_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    """Mocka o tempo de criação e atualização de um modelo no banco de dados.

    Returns:
        datetime: Tempo mockado para utilização nos testes
    """
    return _mock_db_time


@pytest.fixture
def token(client, user):
    """Gera um token de autenticação para o usuário fornecido.

    Args:
        client (TestClient): Cliente de teste para fazer requisições.
        user (User): Usuário para gerar o token.

    Returns:
        str: Token de autenticação no formato 'Bearer token'.
    """
    response = client.post(
        'auth/token', data={'username': user.email, 'password': PASSWORD}
    )
    token = response.json()
    return f'{token['token_type']} {token['access_token']}'
