# Short Url Generator

Small URL shortener service implemented in Python.

Need to generate short URLs quickly and easily? This repository contains an API (FastAPI-style) including models, schemas, and utilities for handling Redis caching and database persistence (Alembic migrations included).

## Features

- Endpoints to create and resolve short URLs.
- Redis integration (cache with TTL) for fast lookups.
- Database migrations managed with Alembic for SQL databases.
- Logging file to monitor application activities and errors.
- Rate limiting to prevent service abuse — maximum 5 requests per minute.

## Features to be implemented

- [ ] Multi-database support (“MySQL, MongoDB”) .
- [ ] Repository layers (“PostgreSQL, MySQL, MongoDB”).
- [ ] Docker development files.

---

### Requirements

You need the following to run this project:

- Python 3.13 or higher (see `.python-version`)
- Database server (Postgres is the only supported SQL database for now)
- Project dependencies (see `pyproject.toml` or `requirements.txt`)
- Redis server (not required if you will not use Redis)
- [uv](https://docs.astral.sh/uv/) for managing virtual environments (recommended)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SalomonRN/Short-Url-Generator.git
   cd Short-Url-Generator
   ```

2. **Create and activate a virtual environment, then install dependencies (choose either `uv` or `pip` for this step):**
   If you don’t have `uv` installed, install it with pip:

   #### Using uv

   ```bash
   pip install uv
   ```

   or see [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

   Then, use `uv` to create and activate a virtual environment:

   ```bash
   uv venv
   .venv\Scripts\activate
   ```

   Now, install the dependencies:

   ```bash
    uv sync
   ```

   #### Using pip

   Or, if you prefer to use `pip` directly, you can use `venv` module to create a virtual environment.

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root and add the required environment variables.
   See `.env.example` for reference

   > **Note:** URI_MONGO, REDIS_HOST and REDIS_PASSWORD are optional depending on your usage.

4. **Run database migrations:**
   > ⚠️ **IMPORTANT** ⚠️
   > This project uses Alembic for SQL-database migrations, but Alembic does not support async DB drivers directly. If your DATABASE_URL uses an async driver (for example postgresql+asyncpg, mysql+aiomysql, or sqlite+aiosqlite), Alembic must use a synchronous DBAPI to run migrations. The repository includes logic in `env.py` that converts an async URL from the environment into an appropriate sync URL (for example postgresql+asyncpg → postgresql+psycopg2) so Alembic can run normally. If you plan to run migrations, please review `env.py`, inside the alembic folder, to understand how the async → sync URL conversion is handled.
   > If you are using a SQL database, first you have to run the migrations and apply them:

To create a new migration, open a terminal in the project root and run:

```bash
alembic revision --autogenerate -m "your message"
```

Then apply the migrations with:

```bash
alembic upgrade head
```

For more details, see the [Alembic Migrations Guide](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

## Main Dependencies

- [FastAPI](https://fastapi.tiangolo.com/) - Framework
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - SQL migrations tool
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database interactions
- [Redis-py](https://pypi.org/project/redis/) - Redis client
- [asyncpg](https://pypi.org/project/asyncpg/) - Async Postgres driver
- [Slowapi](https://pypi.org/project/slowapi/) - Rate limiting

All dependencies are listed in `pyproject.toml`.

---

## Redis usage

This project uses Redis as a caching layer to store short URL mappings temporarily for faster access. If Redis is unavailable when the server starts, the application will still run, but caching functionalities will be disabled and all requests will hit the database directly. If you want the server to exit if Redis is not reachable at startup, you can change the `redis_exit_on_fail` variable in `main.py` to `True`.

---

## Logging

The application uses a logging system to record important events and errors. Logs are stored in the `logs` folder. The application creates a new daily log file named with the current date (e.g., `2024-06-15.log`). Make sure to check this file for debugging and monitoring purposes.

## Run the application

This project is intended to run under an ASGI server (e.g. Uvicorn). Typical command:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 80
```

If you’re not using `uv`, you can run:

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

(Adjust `main:app` if your entrypoint or app variable name differs.)
