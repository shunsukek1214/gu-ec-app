"use client";

import { useEffect, useState } from "react";

type CartItem = {
  cart_item_id: number;
  product_name: string;
  color_name: string;
  size_name: string;
  quantity: number;
  stock_quantity: number;
  line_total: string | number;
};

type CartData = {
  cart_items: CartItem[];
  subtotal: string | number;
  tax: string | number;
  total: string | number;
};

export default function CartClient() {
  const [cart, setCart] = useState<CartData | null>(null);

  const loadCart = async () => {
    const response = await fetch("/api/cart", {
      cache: "no-store",
    });

    const data = await response.json();

    if (response.ok) {
      setCart(data);
    }
  };

  useEffect(() => {
    loadCart();
  }, []);

  if (!cart) {
    return <p>読み込み中...</p>;
  }

  return (
    <main>
      <h1>カート</h1>

      {cart.cart_items.length === 0 && <p>カートは空です。</p>}

      {cart.cart_items.map((item) => (
        <div key={item.cart_item_id}>
          <h2>{item.product_name}</h2>

          <p>
            {item.color_name}
            {" / "}
            {item.size_name}
          </p>

          <p>数量：{item.quantity}</p>

          <button
            disabled={item.quantity <= 1}
            onClick={async () => {
              const response = await fetch(
                `/api/cart/items/${item.cart_item_id}`,
                {
                  method: "PATCH",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    quantity: item.quantity - 1,
                  }),
                },
              );

              if (response.ok) {
                setCart(await response.json());
              }
            }}
          >
            −
          </button>

          <button
            disabled={item.quantity >= 5}
            onClick={async () => {
              const response = await fetch(
                `/api/cart/items/${item.cart_item_id}`,
                {
                  method: "PATCH",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    quantity: item.quantity + 1,
                  }),
                },
              );

              if (response.ok) {
                setCart(await response.json());
              }
            }}
          >
            ＋
          </button>

          <button
            onClick={async () => {
              const response = await fetch(
                `/api/cart/items/${item.cart_item_id}`,
                {
                  method: "DELETE",
                },
              );

              if (response.ok) {
                setCart(await response.json());
              }
            }}
          >
            削除
          </button>

          <p>小計： ¥{Number(item.line_total).toLocaleString()}</p>
        </div>
      ))}

      <hr />

      <p>商品小計： ¥{Number(cart.subtotal).toLocaleString()}</p>

      <p>消費税： ¥{Number(cart.tax).toLocaleString()}</p>

      <p>合計： ¥{Number(cart.total).toLocaleString()}</p>
    </main>
  );
}
