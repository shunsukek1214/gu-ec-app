from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.db.database import get_db
from app.schemas.cart import (
    CartAddResponse,
    CartItemCreateRequest,
    CartItemUpdateRequest,
    CartResponse,
)
from app.services.cart_service import (
    add_cart_item,
    build_cart_response,
    delete_cart_item,
    update_cart_item,
)

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)

#ログイン中ユーザーのカートに商品を追加する
@router.post(
    "/items",
    response_model=CartAddResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cart_item(
    request: CartItemCreateRequest,
    #JWTからログイン中ユーザーのuser_idを取得
    #フロントからuser_idは受け取らない！
    user_id: int = Depends(
        get_current_user_id
    ),
    db: Session = Depends(get_db),
):
    return add_cart_item(
        db=db,
        user_id=user_id,
        variant_id=request.variant_id,
        quantity=request.quantity,
    )

#ログイン中ユーザーの現在のカート内容を取得する
@router.get(
    "",
    response_model=CartResponse,
)
def get_cart(
    #JWTからログイン中ユーザーのuser_idを取得
    #フロントからuser_idは受け取らない！
    user_id: int = Depends(
        get_current_user_id
    ),
    db: Session = Depends(get_db),
):
    return build_cart_response(
        db=db,
        user_id=user_id,
    )

#カートに入っている特定の商品明細の数量を変更する
@router.patch(
    "/items/{cart_item_id}",
    response_model=CartResponse,
)
def patch_cart_item(
    cart_item_id: int,
    request: CartItemUpdateRequest,
    user_id: int = Depends(
        get_current_user_id
    ),
    db: Session = Depends(get_db),
):
    return update_cart_item(
        db=db,
        user_id=user_id,
        cart_item_id=cart_item_id,
        quantity=request.quantity,
    )

#カートに入っている特定の商品を削除する
@router.delete(
    "/items/{cart_item_id}",
    response_model=CartResponse,
)
def remove_cart_item(
    cart_item_id: int,
    user_id: int = Depends(
        get_current_user_id
    ),
    db: Session = Depends(get_db),
):
    return delete_cart_item(
        db=db,
        user_id=user_id,
        cart_item_id=cart_item_id,
    )