import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function PostLoginPage() {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }
  //未登録の場合
  if (session.registrationRequired) {
    redirect("/confirmation");
  }
  //登録済みの場合はホームへ
  if (session.guApiJwt) {
    redirect("/home");
  }

  redirect("/login");
}
