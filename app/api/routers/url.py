from fastapi import APIRouter, Depends, Header, HTTPException, Query, File, Path, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from app.models.url import Url
from app.core.schemas.url import InUrl, OutUrl
from app.core.db.session import get_session
from app.utils.base32 import encode
from app.utils.limiter import limiter
from app.utils.redisclient import get_value, set_value


url_router = APIRouter(prefix="/url", tags=["Url"])


async def get_url(session: AsyncSession, tiny_url: str):
    res = await session.execute(select(Url).where(Url.short_url == tiny_url))
    return res.scalar_one_or_none()

async def get_large_url(tiny_url: str = Path(), session=Depends(get_session)):

    url_in_cache: bytes = await get_value(tiny_url)
    if url_in_cache:
        print("Url sacada desde Redis")
        return url_in_cache.decode("utf-8")

    url = await get_url(session, tiny_url)
    if url:
        
        await set_value(tiny_url, url.large_url)
        print("Url sacada desde la base de datos")
        return url.large_url
    raise HTTPException(404, "Url does not exits.")

async def get_next_id(session: AsyncSession):
    result = await session.execute(text("SELECT nextval('urls_id_seq');"))
    return result.scalar()


@url_router.get("/{tiny_url}")
@limiter.limit("5/minute")
async def redirect(request: Request, tiny_url: str, large_url: str = Depends(get_large_url)):
    return RedirectResponse(large_url, status_code=301)

@url_router.post("/", response_model=OutUrl, status_code=201)
@limiter.limit("5/minute")
async def create_url(request: Request, model_url: InUrl, session_db=Depends(get_session)):
    id = await get_next_id(session_db)
    tinty_url = encode(int(id))

    try:
        session_db.add(Url(id=id, short_url=tinty_url, large_url=str(model_url.large_url)))
        await session_db.commit()
    except Exception as error:
        print(type(error))
        raise HTTPException(500, "Algo salió mal, intentalo nuevamente mas tarde.")

    return OutUrl(**model_url.model_dump(), tiny_url=tinty_url)
