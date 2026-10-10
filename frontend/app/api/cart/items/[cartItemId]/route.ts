import { NextResponse } from "next/server";
import { auth } from "@/auth";

export async function PATCH(
  request: Request,
  context: {
    params: Promise<{
      cartItemId: string;
    }>;
  },
) {
  const session = await auth();

  if (!session?.guApiJwt) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { cartItemId } = await context.params;

  const body = await request.json();

  const response = await fetch(
    `${process.env.GU_API_BASE_URL}/cart/items/${cartItemId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.guApiJwt}`,
      },
      body: JSON.stringify(body),
    },
  );

  const data = await response.json();

  return NextResponse.json(data, {
    status: response.status,
  });
}

export async function DELETE(
  _request: Request,
  context: {
    params: Promise<{
      cartItemId: string;
    }>;
  },
) {
  const session = await auth();

  if (!session?.guApiJwt) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { cartItemId } = await context.params;

  const response = await fetch(
    `${process.env.GU_API_BASE_URL}/cart/items/${cartItemId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${session.guApiJwt}`,
      },
    },
  );

  const data = await response.json();

  return NextResponse.json(data, {
    status: response.status,
  });
}
