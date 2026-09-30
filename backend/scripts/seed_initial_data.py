from decimal import Decimal

from app.db.database import SessionLocal
from app.models import (
    Product,
    ProductColor,
    ProductSize,
    Category,
    ProductVariant,
    ProductImage,
    ProductCategory,
)

def main():
    db = SessionLocal()

    try:
        existing_product = (
            db.query(Product)
            .filter(Product.name == "クルーネックTシャツ")  #productsからクルーネックTシャツを探す
            .first()
        )

        if existing_product:
            print("クルーネックTシャツはすでに存在します。")
            return
        


        white = ProductColor(
            color_code="00",
            color_name="WHITE",
        )

        black = ProductColor(
            color_code="09",
            color_name="BLACK",
        )

        db.add_all([white, black])

        size_m = ProductSize(
            size_name="M",
            display_order=1,
        )

        size_l = ProductSize(
            size_name="L",
            display_order=2,
        )

        db.add_all([size_m, size_l])

        tops = Category(
            category_name="トップス",
            category_slug="tops",
        )

        db.add(tops)

        product = Product(
            name="クルーネックTシャツ",
            price=Decimal("1990"),
            description="シンプルで着回しやすいクルーネックTシャツです。",
        )

        db.add(product)

        db.flush()  # product IDを獲得

        white_m = ProductVariant(
            product_id=product.product_id,
            color_id=white.color_id,
            size_id=size_m.size_id,
            stock_quantity=10,
        )

        white_l = ProductVariant(
            product_id=product.product_id,
            color_id=white.color_id,
            size_id=size_l.size_id,
            stock_quantity=10,
        ) 

        black_m = ProductVariant(
            product_id=product.product_id,
            color_id=black.color_id,
            size_id=size_m.size_id,
            stock_quantity=10,
        )

        black_l = ProductVariant(
            product_id=product.product_id,
            color_id=black.color_id,
            size_id=size_l.size_id,
            stock_quantity=10,
        )

        db.add_all([white_m, white_l, black_m, black_l])

        product_category = ProductCategory(
            product_id=product.product_id,
            category_id=tops.category_id,
        )

        db.add(product_category)

        white_image = ProductImage(
            product_id=product.product_id,
            color_id=white.color_id,
            image_url="https://example.com/images/white_tshirt.jpg",
            display_order=1,
        )

        black_image = ProductImage(
            product_id=product.product_id,
            color_id=black.color_id,
            image_url="https://example.com/images/black_tshirt.jpg",
            display_order=1,
        )

        db.add_all([white_image, black_image])

        db.commit()
        print("初期データの投入が完了しました。")
        print(f"Product ID: {product.product_id}, Name: {product.name}, Price: {product.price}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
