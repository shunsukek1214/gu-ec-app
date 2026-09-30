import "next-auth";
import "next-auth/jwt";

declare module "next-auth" {
  interface Session {
    guApiJwt?: string;
    registrationRequired?: boolean;
    registrationToken?: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    guApiJwt?: string;
    registrationRequired?: boolean;
    registrationToken?: string;
  }
}
