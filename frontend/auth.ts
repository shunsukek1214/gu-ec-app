import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

type BackendAuthResponse = {
  registration_required: boolean;
  gu_api_jwt?: string | null;
  registration_token?: string | null;
};

export const { handlers, auth, signIn, signOut } = NextAuth({
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "jwt",
  },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  //jwt callback
  callbacks: {
    async jwt({ token, account, trigger, session }) {
      //ログイン直後だけ
      if (account?.provider === "google" && account.id_token) {
        //POST/authを呼ぶ
        const response = await fetch(`${process.env.GU_API_BASE_URL}/auth`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id_token: account.id_token,
          }),
        });
        //エラー確認
        if (!response.ok) {
          throw new Error(`FastAPI /auth failed: ${response.status}`);
        }
        //JSONを受け取る
        const data = (await response.json()) as BackendAuthResponse;
        //登録状態を保存
        token.registrationRequired = data.registration_required;
        //登録済みの場合
        if (!data.registration_required) {
          token.guApiJwt = data.gu_api_jwt ?? undefined;
          token.registrationToken = undefined;
        } else {
          //未登録の場合
          token.registrationToken = data.registration_token ?? undefined;
          token.guApiJwt = undefined;
        }
      }
      if (trigger === "update" && session) {
        if (typeof session.guApiJwt === "string") {
          token.guApiJwt = session.guApiJwt;
        }

        if (typeof session.registrationRequired === "boolean") {
          token.registrationRequired = session.registrationRequired;
        }

        if (session.registrationToken === null) {
          token.registrationToken = undefined;
        }
      }
      return token;
    },
    async session({ session, token }) {
      session.guApiJwt =
        typeof token.guApiJwt === "string" ? token.guApiJwt : undefined;

      session.registrationRequired =
        typeof token.registrationRequired === "boolean"
          ? token.registrationRequired
          : undefined;

      session.registrationToken =
        typeof token.registrationToken === "string"
          ? token.registrationToken
          : undefined;

      return session;
    },
  },
});
