from dotenv import load_dotenv

load_dotenv()

import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils.redisclient import setup_redis_connection, ping_redis, close_redis
from app.utils.logger import logger
from app.core.db.session import create_session, ping_database
from app.api.routers import url_router
from app.utils.limiter import limiter
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    redis_exit_on_fail = os.getenv("REDIS_EXIT") # This handle the exit behavior if redis is not reachable at startup
    try:
        logger.info("Iniciando servidor.")
        await setup_redis_connection()
        await ping_redis(redis_exit_on_fail)

        await create_session()
        await ping_database()
    except Exception as error:
        logger.error(f"Servidor deteniendose por {error}", exc_info=True)
        raise RuntimeError("Algo salió mal iniciando el servidor...")

    logger.info("Servidor iniciado.")

    yield

    logger.info("Cerrando conexiones a los servicios.")
    await close_redis()
    logger.info("Cerrando aplicación...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('FRONT_URL', '*')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.include_router(url_router)


@app.get("/")
async def index():
    return {"msg": "Hola Mundo"}


if __name__ == "__main__":
    # uv run fastapi dev main.py
    # uv run uvicorn main:app --reload
    # uvicorn main:app --host 0.0.0.0 --port 80
    # uv run fastapi run --workers 4 main.py
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=80)
