"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";

export default function RegistrationPage() {
  const router = useRouter();
  const { update } = useSession();

  const [postCode, setPostCode] = useState("");
  const [birthday, setBirthday] = useState("");
  const [sex, setSex] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const response = await fetch("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        post_code: postCode,
        birthday,
        sex,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error(data);
      return;
    }

    await update({
      guApiJwt: data.gu_api_jwt,
      registrationRequired: false,
      registrationToken: null,
    });

    router.push("/end");
  };

  return (
    <main>
      <h1>会員情報登録</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>郵便番号</label>

          <input
            value={postCode}
            onChange={(event) => setPostCode(event.target.value)}
            required
          />
        </div>

        <div>
          <label>生年月日</label>

          <input
            type="date"
            value={birthday}
            onChange={(event) => setBirthday(event.target.value)}
            required
          />
        </div>

        <div>
          <label>性別</label>

          <select
            value={sex}
            onChange={(event) => setSex(event.target.value)}
            required
          >
            <option value="">選択してください</option>

            <option value="male">男性</option>

            <option value="female">女性</option>

            <option value="other">その他</option>
          </select>
        </div>

        <button type="submit">登録</button>
      </form>
    </main>
  );
}
