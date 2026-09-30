from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.db.database import get_db
from app.schemas.product import (
    ProductListResponse,
    ProductDetailResponse,
)
from app.services.product_service import (
    search_products,
    get_product_detail,
)

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

#GET/products
@router.get(
    "",
    response_model=ProductListResponse,
)
def get_products(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id), 
):
    return search_products(
        db = db,
        keyword=keyword,
        category=category,
    )

#GET/products/{product_id}
@router.get(
    "/{product_id}",
    response_model = ProductDetailResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    product = get_product_detail(
        db=db,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    return product