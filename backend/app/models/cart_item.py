from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from app.db.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint('user_id', 'variant_id'),)

    cart_item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    variant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("product_variants.variant_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
