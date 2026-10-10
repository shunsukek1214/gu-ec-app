import Link from "next/link";

type CartAddedPageProps = {
  searchParams: Promise<{
    product_id?: string;
  }>;
};

export default async function CartAddedPage({
  searchParams,
}: CartAddedPageProps) {
  const params = await searchParams;

  const productId = params.product_id;

  return (
    <main>
      <h1>カートに追加しました</h1>

      <p>
        <Link href="/cart">カートを見る</Link>
      </p>

      {productId ? (
        <p>
          <Link href={`/products/${productId}`}>お買い物を続ける</Link>
        </p>
      ) : (
        <p>
          <Link href="/home">お買い物を続ける</Link>
        </p>
      )}
    </main>
  );
}
