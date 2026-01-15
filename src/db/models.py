import uuid

from sqlalchemy import Column, Integer, String, BigInteger, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

__all__ = ["Btc"]

class Btc(Base):
    __tablename__ = 'btc'
    btc_id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True, unique=True)
    btc_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    symbol = Column(String)
