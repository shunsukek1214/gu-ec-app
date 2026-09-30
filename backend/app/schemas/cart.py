from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field

class CartItemCreateRequest(BaseModel):
    variant_id: int
    quantity: int = Field(ge=1, le=5)

class CartItemUpdateRequest(BaseModel):
    quantity: int = Field(ge=1, le=5)

class CartItemResponse(BaseModel):
    cart_item_id: int
    variant_id: int

    product_id: int
    product_name: str
    price: Decimal

    image_url: Optional[str]

    color_id: int
    color_name: str

    size_id: int
    size_name: str

    quantity: int
    stock_quantity: int
    line_total: Decimal

class CartResponse(BaseModel):
    cart_items: List[CartItemResponse] = Field(
        default_factory=list
    )

    subtotal: Decimal
    tax: Decimal
    total: Decimal

class CartAddResponse(BaseModel):
    cart_item: CartItemResponse
    cart_summary: CartResponse