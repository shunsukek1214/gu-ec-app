import Link from "next/link";
import { auth } from "@/auth";
import { redirect } from "next/navigation";

import type { ProductListResponse } from "@/types/product";

type ResultsPageProps = {
  searchParams: Promise<{
    keyword?: string;
    category?: string;
  }>;
};

export default async function ResultsPage({ searchParams }: ResultsPageProps) {
  const session = await auth();

  if (!session?.guApiJwt) {
    redirect("/login");
  }

  const params = await searchParams;

  const keyword = params.keyword?.trim() ?? "";

  const category = params.category?.trim() ?? "";

  const query = new URLSearchParams();

  if (keyword) {
    query.set("keyword", keyword);
  }

  if (category) {
    query.set("category", category);
  }

  const response = await fetch(
    `${process.env.GU_API_BASE_URL}/products?${query.toString()}`,
    {
      headers: {
        Authorization: `Bearer ${session.guApiJwt}`,
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  const data = (await response.json()) as ProductListResponse;

  return (
    <main>
      <h1>検索結果</h1>

      {keyword && (
        <p>
          キーワード：
          {keyword}
        </p>
      )}

      {category && (
        <p>
          カテゴリ：
          {category}
        </p>
      )}

      {data.products.length === 0 && <p>該当する商品はありません。</p>}

      {data.products.map((product) => (
        <article key={product.product_id}>
          {product.image_url && (
            <img src={product.image_url} alt={product.name} width={180} />
          )}

          <h2>{product.name}</h2>

          <p>¥{Number(product.price).toLocaleString()}</p>

          <p>
            カラー：
            {product.colors.map((color) => color.color_name).join(" / ")}
          </p>

          <p>{product.in_stock ? "在庫あり" : "在庫なし"}</p>

          <Link href={`/products/${product.product_id}`}>商品詳細を見る</Link>

          <hr />
        </article>
      ))}

      <Link href="/home">ホームへ戻る</Link>
    </main>
  );
}
