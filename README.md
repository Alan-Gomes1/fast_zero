# Fast Zero

API desenvolvida com FastAPI para gerenciar usuários, incluindo autenticação e operações CRUD.

## Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI**: Framework web para construir APIs.
- **SQLAlchemy**: ORM para interagir com o banco de dados.
- **Alembic**: Ferramenta para migrações de banco de dados.
- **Pydantic**: Para validação de dados.
- **JWT (JSON Web Tokens)**: Para autenticação.
- **Pwdlib**: Para hashing de senhas.
- **Poetry**: Para gerenciamento de dependências.
- **Ruff**: Para linting e formatação de código.
- **Pytest**: Para testes automatizados.

## Funcionalidades

- Criação de usuários.
- Leitura de usuários (com paginação).
- Atualização de usuários.
- Exclusão de usuários.
- Autenticação de usuários com JWT.
- Refresh de tokens de acesso.

## Como Executar o Projeto

### Pré-requisitos

- Python 3.12+
- Poetry

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/fast_zero.git
   cd fast_zero
   ```

2. Crie e configure o ambiente virtual com Poetry:
   ```bash
   poetry shell
   poetry install
   ```

3. Crie o arquivo `.env` a partir do exemplo e preencha as variáveis de ambiente:
   ```bash
   cp .env-example .env
   ```

4. Execute as migrações do banco de dados:
   ```bash
   poetry run alembic upgrade head
   ```

### Execução

Para iniciar o servidor de desenvolvimento, execute:

```bash
poetry run task run
```

A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

### Testes

Para executar os testes automatizados, utilize o comando:

```bash
poetry run task test
```
