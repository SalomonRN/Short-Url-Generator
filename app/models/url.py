from app.models.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Sequence


class Url(Base):
    __tablename__ = "urls"
    id: Mapped[int] = mapped_column(Integer, Sequence("urls_id_seq", start=0, minvalue=0, increment=1),  primary_key=True)
    short_url: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)
    large_url: Mapped[str] = mapped_column(String(256), nullable=False)
