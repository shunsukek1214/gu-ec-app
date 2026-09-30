from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class ProductSize(Base):
    __tablename__ = "product_size"

    size_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    size_name: Mapped[str] = mapped_column(String(20), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
