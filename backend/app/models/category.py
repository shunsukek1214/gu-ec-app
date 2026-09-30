from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)