//カート件数、商品検索
import Link from "next/link";
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function HomePage() {
  const session = await auth();

  if (!session?.guApiJwt) {
    redirect("/login");
  }

  const response = await fetch(`${process.env.GU_API_BASE_URL}/user_info`, {
    headers: {
      Authorization: `Bearer ${session.guApiJwt}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user info");
  }

  const data = await response.json();

  return (
    <main>
      <h1>{data.user.name}さん、ようこそ</h1>

      <p>
        カート件数：
        {data.cart_count}
      </p>

      <p>
        <Link href="/cart">カートを見る</Link>
      </p>

      <hr />

      <h2>商品を探す</h2>

      <form action="/results" method="get">
        <input type="text" name="keyword" placeholder="例：Tシャツ" />

        <button type="submit">検索</button>
      </form>

      <h2>カテゴリ</h2>

      <Link href="/results?category=tops">トップス</Link>
    </main>
  );
}
