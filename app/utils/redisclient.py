import os
import asyncio
import datetime
from rich import print
import redis.asyncio as redis
from redis.exceptions import ConnectionError, AuthenticationError
from app.utils.logger import logger

REDIS_CONNECTED = False
redis_connection = None

async def setup_redis_connection():
    global REDIS_CONNECTED, redis_connection
    print("[green]INFO: [/green]Configurando conexión a Redis...")
    REDIS_URL = os.getenv("REDIS_URL")
    
    if not REDIS_URL:
        logger.warning("REDIS_URL no está configurado en las variables de entorno.")
        return
    
    redis_connection = redis.from_url(REDIS_URL)

async def ping_redis(exit=True) -> bool:
    global REDIS_CONNECTED
    if not redis_connection:
        if exit:
            raise RuntimeError("No se pudó conectar a redis, revisa si las variables de entorno de REDIS_HOST y REDIS_PASS si se encuentran establecidas.")
        logger.warning("Conexion no establecida. Servidor sigue funcionando sin Redis.")
        return
    try:
        REDIS_CONNECTED = await redis_connection.ping()
        return REDIS_CONNECTED
       
    except AuthenticationError as error:
        if exit:
            logger.error("Error de autenticación con Redis. ¿Las credenciales son correctas?")
            raise RuntimeError(error)
        
        logger.warning("Las credenciales de Redis son incorrectas. El servidor sigue ejecutandose sin tener Redis en servicio.")
        print("[yellow]WARNING: [/yellow] No hay conexion a redis. El servidor sigue ejecutandose sin tener Redis en servicio.")
    except ConnectionError as error:
        if exit:
            logger.error("No se pudó establecer conexión con redis. ¿Redis está corriendo? ¿El host es el correcto?")
            raise RuntimeError(error)
        
        logger.warning("Redis parece no estar disponible. El servidor sigue ejecutandose sin tener Redis en servicio.")
        print("[yellow]WARNING: [/yellow] Redis parece no estar disponible. El servidor sigue ejecutandose sin tener Redis en servicio.")
    
    except AttributeError as error:
        if exit:
            logger.error("No se pudó establecer conexión con redis. Revisa la configuración y si Redis está corriendo.")
            raise RuntimeError(error)
        
        logger.warning("No hay conexion a redis. El servidor sigue ejecutandose sin tener Redis en servicio.")
        print("[yellow]WARNING: [/yellow] No hay conexion a redis. El servidor sigue ejecutandose sin tener Redis en servicio.")


def is_redis_active(func):
    """Decorator that only allows the wrapped function to run when REDIS_CONNECTED is True.

    Supports both async and sync callables. If REDIS_CONNECTED is False, the wrapper returns
    None.
    """

    import inspect

    if inspect.iscoroutinefunction(func):
        async def async_wrapper(*args, **kwargs):
            if not REDIS_CONNECTED:
                return None
            return await func(*args, **kwargs)

        return async_wrapper

    else:
        def sync_wrapper(*args, **kwargs):
            if not REDIS_CONNECTED:
                return None
            return func(*args, **kwargs)

        return sync_wrapper


@is_redis_active
async def set_value(key: str, value: str, expire_in=datetime.timedelta(days=1)) -> bool:

    try:
        return await redis_connection.set(key, value, ex=expire_in)
    except ConnectionError:
        return False


@is_redis_active
async def get_value(key: str) -> bytes | None:
    try:
        return await redis_connection.get(key)
    except Exception as error:
        return 0
   


async def close_redis():
    global REDIS_CONNECTED
    await redis_connection.close()
    REDIS_CONNECTED = False


if __name__ == "__main__":
    
    async def main():

        await ping_redis(exit=False)
        res = await set_value("llave", "valor")
        print(res)


    asyncio.run(main())
