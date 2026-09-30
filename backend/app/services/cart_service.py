from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import (
    CartItem,
    Product,
    ProductColor,
    ProductImage,
    ProductSize,
    ProductVariant,
)

#消費税１０％
TAX_RATE = Decimal("0.10")

#カート全体を取得する関数
def build_cart_response(
        db: Session,
        user_id: int,
):
    rows = (
        db.query(
            CartItem,
            ProductVariant,
            Product,
            ProductColor,
            ProductSize,
        )
        .join(
            ProductVariant,
            CartItem.variant_id == ProductVariant.variant_id,
        )
        .join(
            Product,
            ProductVariant.product_id == Product.product_id,
        )
        .join(
            ProductColor,
            ProductVariant.color_id == ProductColor.color_id
        )
        .join(
            ProductSize,
            ProductVariant.size_id == ProductSize.size_id
        )
        .filter(
            CartItem.user_id == user_id
        )
        .all()
    )

    cart_items = []
    subtotal = Decimal("0")

    for (
        cart_item,
        variant,
        product,
        color,
        size,
    ) in rows:
        #商品画像を取得
        image = (
            db.query(ProductImage)
            .filter(
                ProductImage.product_id == product.product_id,
                ProductImage.color_id == color.color_id,
            )
            .order_by(
                ProductImage.display_order
            )
            .first()
        )
        #商品画像が無ければ商品共通画像を探す
        if image is None:
            image = (
                db.query(ProductImage)
                .filter(
                    ProductImage.product_id == product.product_id,
                    ProductImage.color_id.is_(None)
                )
                .order_by(
                    ProductImage.display_order
                )
                .first()
            )

    #小計
    line_total = (
        product.price * cart_item.quantity
    )

    subtotal += line_total

    cart_items.append(
        {
            "cart_item_id": cart_item.cart_item_id,
            "variant_id": variant.variant_id,
            "product_id": product.product_id,
            "product_name": product.name,
            "price": product.price,
            "image_url": image.image_url
            if image
            else None,
            "color_id": color.color_id,
            "color_name": color.color_name,
            "size_id": size.size_id,
            "size_name": size.size_name,
            "quantity": cart_item.quantity,
            "stock_quantity": variant.stock_quantity,
            "line_total": line_total,
        }
    )

    tax = (
        subtotal * TAX_RATE
    ).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP,
    )

    total = subtotal + tax

    return {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
    }

#数量追加
def add_cart_item(
        db: Session,
        user_id: int,
        variant_id: int,
        quantity: int,
):
    variant = (
        db.query(ProductVariant)
        .filter(
            ProductVariant.variant_id == variant_id
        )
        .first()
    )

    if variant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found",
        )
    
    existing_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == user_id,
            CartItem.variant_id == variant_id,
        )
        .first()
    )

    if existing_item:
        new_quantity = (
            existing_item.quantity + quantity
        )
    else:
        new_quantity = quantity

    #数量上限と在庫確認
    if new_quantity > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum quantity is 5",
        )
    
    if new_quantity > variant.stock_quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient stock",
        )
    
    #DB登録・更新
    if existing_item:
        existing_item.quantity = new_quantity
        cart_item = existing_item
    else:
        cart_item = CartItem(
            user_id=user_id,
            variant_id=variant_id,
            quantity=quantity,
        )

        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    #カート全体を取得
    cart_summary = build_cart_response(
        db=db,
        user_id=user_id,
    )

    added_item = next(
        item 
        for item in cart_summary["cart_items"]
        if item["cart_item_id"] == cart_item.cart_item_id
    )

    return {
        "cart_item": added_item,
        "cart_summary": cart_summary,
    }


#数量変更
def update_cart_item(
        db:Session,
        user_id: int,
        cart_item_id: int,
        quantity: int,
):
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_item_id == cart_item_id,
            CartItem.user_id == user_id,
        )
        .first()
    )

    if cart_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )
    
    variant = (
        db.query(ProductVariant)
        .filter(
            ProductVariant.variant_id == cart_item.variant_id
        )
        .first()
    )

    if quantity > variant.stock_quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient stock",
        )
    
    cart_item.quantity = quantity

    db.commit()

    return build_cart_response(
        db=db,
        user_id=user_id,
    )

#削除
def delete_cart_item(
    db: Session,
    user_id: int,
    cart_item_id: int,
):
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_item_id
            == cart_item_id,
            CartItem.user_id
            == user_id,
        )
        .first()
    )

    if cart_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )
    
    db.delete(cart_item)
    db.commit()

    return build_cart_response(
        db=db,
        user_id=user_id,
    )