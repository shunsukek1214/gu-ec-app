from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    address_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user_address.address_id"), nullable=False)
    subtotal_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 0), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 0), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 0), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), nullable=False)
    ordered_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    status: Mapped[str] = mapped_column(String(30), nullable=False)