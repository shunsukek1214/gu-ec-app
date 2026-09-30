import Link from "next/link";
import { signOut } from "@/auth";

export default function ConfirmationPage() {
  return (
    <main>
      <h1>新規会員登録</h1>

      <p>新規会員登録しますか？</p>

      <Link href="/registration">はい</Link>

      <form
        action={async () => {
          "use server";

          await signOut({
            redirectTo: "/login",
          });
        }}
      >
        <button type="submit">いいえ</button>
      </form>
    </main>
  );
}
