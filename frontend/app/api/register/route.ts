import { NextResponse } from "next/server";

import { auth } from "@/auth";

export async function POST(request: Request) {
  const session = await auth();

  if (!session?.registrationToken) {
    return NextResponse.json(
      {
        error: "Registration token is missing",
      },
      {
        status: 401,
      },
    );
  }

  const body = await request.json();

  const response = await fetch(`${process.env.GU_API_BASE_URL}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.registrationToken}`,
    },
    body: JSON.stringify(body),
  });

  const data = await response.json();

  return NextResponse.json(data, {
    status: response.status,
  });
}
