from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, text, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from app.db.database import Base

class ProductVariant(Base):
    __tablename__ = "product_variants"
    __table_args__ = (UniqueConstraint('product_id', 'color_id', 'size_id', name='uq_product_variant'),)

    variant_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.product_id"), nullable=False)
    color_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("product_color.color_id"), nullable=False)
    size_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("product_size.size_id"), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False,  server_default=text("0"))