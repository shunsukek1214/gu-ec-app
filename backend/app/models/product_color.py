from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class ProductColor(Base):
    __tablename__ = "product_color"

    color_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    color_code: Mapped[str] = mapped_column(String(20), nullable=False)
    color_name: Mapped[str] = mapped_column(String(50), nullable=False)
