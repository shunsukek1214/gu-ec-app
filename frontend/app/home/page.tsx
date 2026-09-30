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
      <h1>{data.user.name}さん、 ようこそ</h1>

      <p>
        カート件数：
        {data.cart_count}
      </p>
    </main>
  );
}
