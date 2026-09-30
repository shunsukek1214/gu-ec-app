from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field

#商品の色を表すレスポンス
class ProductColorResponse(BaseModel):
    color_id: int
    color_code: str
    color_name: str

#検索結果の商品の情報を表すレスポンス
class ProductListItemResponse(BaseModel):
    product_id: int
    name: str
    price: Decimal
    image_url: Optional[str] = None
    colors: List[ProductColorResponse] = Field(default_factory=list)
    in_stock: bool  # 在庫があるかどうかを示すフィールド

#検索結果一覧のレスポンスを表すモデル
class ProductListResponse(BaseModel):
    products: List[ProductListItemResponse] = Field(default_factory=list)

#商品のバリエーション情報を表すレスポンス
class ProductVariantResponse(BaseModel):
    variant_id: int
    color_id: int
    color_name: str
    size_id: int
    size_name: str
    stock_quantity: int

#商品画像の情報を表すレスポンス
class ProductImageResponse(BaseModel):
    image_id: int
    color_id: Optional[int]
    image_url: str
    display_order: int

# 商品詳細情報を表すレスポンス
class ProductDetailResponse(BaseModel):
    product_id: int
    name: str
    price: Decimal
    description: Optional[str]
    colors: List[ProductColorResponse] = Field(default_factory=list)
    variants: List[ProductVariantResponse] = Field(default_factory=list)
    images: List[ProductImageResponse] = Field(default_factory=list)