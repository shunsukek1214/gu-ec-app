from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    google_sub: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=False)
    post_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sex: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp(),)
