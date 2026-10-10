#DB検索処理

from typing import Optional

from sqlalchemy.orm import Session

from app.models import (
    Product,
    ProductColor,
    ProductSize,
    ProductVariant,
    ProductImage,
    Category,
    ProductCategory,
)

def search_products(
    db: Session,
    keyword: Optional[str] = None,
    category: Optional[str] = None,
):
    query = db.query(Product)

    #キーワード検索
    if keyword:
        query = query.filter(Product.name.contains(keyword))

    #カテゴリ検索
    if category:
        query = query.join(ProductCategory,
        Product.product_id == ProductCategory.product_id
        ).join(Category,
              ProductCategory.category_id == Category.category_id
              ).filter(Category.category_slug == category)
    
    #検索結果を最大２０件にする
    products = (
        query
        .distinct()
        .limit(20)
        .all()
    )

    results = []    

    for product in products:
        #各商品のカラーを取得
        colors = (
            db.query(ProductColor)
            .join(
                ProductVariant,
                ProductColor.color_id == ProductVariant.color_id
            )
            .filter(
                ProductVariant.product_id == product.product_id
            )
            .distinct()
            .all()
        )

        #在庫があるか確認する
        in_stock = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.product_id == product.product_id,
                ProductVariant.stock_quantity > 0,
            )
            .first()
            is not None
        )

        #代表画像を取得する
        image = (
            db.query(ProductImage)
            .filter(
                ProductImage.product_id == product.product_id,
                ProductImage.display_order == 1,
            )
            .first()
        )

        image_url = image.image_url if image else None

        result = {
            "product_id": product.product_id,
            "name": product.name,
            "price": product.price,
            "image_url": image_url,
            "colors": [
                {
                    "color_id": color.color_id,
                    "color_code": color.color_code,
                    "color_name": color.color_name,
                }
                for color in colors
            ],
            "in_stock": in_stock,
        }

        results.append(result)

    return {"products": results}


#商品詳細
def get_product_detail(
        db: Session,
        product_id: int,
):
    product = (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )
    
    if product is None:
        return None
    
    variants = (
        db.query(
            ProductVariant,
            ProductColor,
            ProductSize,
        )
        .join(
            ProductColor,
            ProductVariant.color_id == ProductColor.color_id,
        )
        .join(
            ProductSize,
            ProductVariant.size_id == ProductSize.size_id,
        )
        .filter(
            ProductVariant.product_id == product_id
        )
        .all()
    )

    colors_by_id = {}

    for variant, color, size in variants:
        colors_by_id[color.color_id] = {
            "color_id": color.color_id,
            "color_code": color.color_code,
            "color_name": color.color_name,
        }

    images = (
        db.query(ProductImage)
        .filter(
            ProductImage.product_id == product_id
        )
        .order_by(
            ProductImage.display_order
        )
        .all()
    )

    return {
        "product_id": product.product_id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "colors": list(colors_by_id.values()),
        "variants": [
            {
                "variant_id": variant.variant_id,
                "color_id": color.color_id,
                "color_name": color.color_name,
                "size_id": size.size_id,
                "size_name": size.size_name,
                "stock_quantity": variant.stock_quantity,
            }
            for variant, color, size in variants
        ],
        "images": [
            {
                "image_id": image.image_id,
                "color_id": image.color_id,
                "image_url": image.image_url,
                "display_order": image.display_order,
            }
            for image in images
        ],
    }