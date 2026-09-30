import Link from "next/link";

export default function EndPage() {
  return (
    <main>
      <h1>ありがとうございました</h1>

      <p>会員登録が完了しました。</p>

      <Link href="/home">ホームへ</Link>
    </main>
  );
}
