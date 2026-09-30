from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, DateTime, DECIMAL, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey

from app.db.database import Base

class ProductCategory(Base):
    __tablename__ = "product_categories"

    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.product_id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.category_id"), primary_key=True)
    
