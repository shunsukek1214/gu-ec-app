from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.database import Base

class UserAddress(Base):
    __tablename__ = "user_address"

    address_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    last_name_kanji: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name_kanji: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name_katakana: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name_katakana: Mapped[str] = mapped_column(String(50), nullable=False)
    post_number: Mapped[str] = mapped_column(String(8), nullable=False)
    prefecture: Mapped[str] = mapped_column(String(20), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    street_address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)