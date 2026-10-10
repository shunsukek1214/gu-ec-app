import Link from "next/link";
import { notFound, redirect } from "next/navigation";

import { auth } from "@/auth";

import AddToCartForm from "./AddToCartForm";

import type { ProductDetailResponse } from "@/types/product";

type ProductPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function ProductPage({ params }: ProductPageProps) {
  const session = await auth();

  if (!session?.guApiJwt) {
    redirect("/login");
  }

  const { id } = await params;

  const productId = Number(id);

  if (!Number.isInteger(productId) || productId <= 0) {
    notFound();
  }

  const response = await fetch(
    `${process.env.GU_API_BASE_URL}/products/${productId}`,
    {
      headers: {
        Authorization: `Bearer ${session.guApiJwt}`,
      },
      cache: "no-store",
    },
  );

  if (response.status === 404) {
    notFound();
  }

  if (!response.ok) {
    throw new Error("Failed to fetch product detail");
  }

  const product = (await response.json()) as ProductDetailResponse;

  const mainImage = product.images[0] ?? null;

  return (
    <main>
      <p>
        <Link href="/results">← 検索結果へ</Link>
      </p>

      <h1>{product.name}</h1>

      {mainImage ? (
        <img src={mainImage.image_url} alt={product.name} width={300} />
      ) : (
        <p>商品画像はありません。</p>
      )}

      <p>¥{Number(product.price).toLocaleString()}</p>

      {product.description && <p>{product.description}</p>}

      <h2>カラー</h2>

      <ul>
        {product.colors.map((color) => (
          <li key={color.color_id}>{color.color_name}</li>
        ))}
      </ul>

      <h2>在庫</h2>

      <ul>
        {product.variants.map((variant) => (
          <li key={variant.variant_id}>
            {variant.color_name}
            {" / "}
            {variant.size_name}
            {" ： "}
            {variant.stock_quantity}個
          </li>
        ))}
      </ul>

      <h2>カートに追加</h2>

      <AddToCartForm
        productId={product.product_id}
        variants={product.variants}
      />
    </main>
  );
}
