import { auth } from "@/auth";
import { redirect } from "next/navigation";

import CartClient from "./CartClient";

export default async function CartPage() {
  const session = await auth();

  if (!session?.guApiJwt) {
    redirect("/login");
  }

  return <CartClient />;
}
