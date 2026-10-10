"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import type { ProductVariant } from "@/types/product";

type AddToCartFormProps = {
  productId: number;
  variants: ProductVariant[];
};

export default function AddToCartForm({
  productId,
  variants,
}: AddToCartFormProps) {
  const router = useRouter();

  const [variantId, setVariantId] = useState<number | null>(null);

  const [quantity, setQuantity] = useState(1);

  const [error, setError] = useState("");

  const selectedVariant = variants.find(
    (variant) => variant.variant_id === variantId,
  );

  const maxQuantity = selectedVariant
    ? Math.min(5, selectedVariant.stock_quantity)
    : 1;

  const quantityOptions = Array.from(
    {
      length: maxQuantity,
    },
    (_, index) => index + 1,
  );

  const addToCart = async () => {
    setError("");

    if (variantId === null) {
      setError("カラー・サイズを選択してください");

      return;
    }

    const response = await fetch("/api/cart/items", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        variant_id: variantId,
        quantity,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setError(data.detail ?? data.error ?? "カート追加に失敗しました");

      return;
    }

    router.push(`/cart_added?product_id=${productId}`);
  };

  return (
    <div>
      <label>カラー・サイズ</label>

      <select
        value={variantId ?? ""}
        onChange={(event) => {
          const value = event.target.value;

          const nextVariantId = value === "" ? null : Number(value);

          setVariantId(nextVariantId);

          setQuantity(1);
          setError("");
        }}
      >
        <option value="">選択してください</option>

        {variants.map((variant) => (
          <option
            key={variant.variant_id}
            value={variant.variant_id}
            disabled={variant.stock_quantity === 0}
          >
            {variant.color_name}
            {" / "}
            {variant.size_name} （在庫 {variant.stock_quantity}）
          </option>
        ))}
      </select>

      <label>数量</label>

      <select
        value={quantity}
        disabled={variantId === null}
        onChange={(event) => setQuantity(Number(event.target.value))}
      >
        {quantityOptions.map((value) => (
          <option key={value} value={value}>
            {value}
          </option>
        ))}
      </select>

      <button
        type="button"
        onClick={addToCart}
        disabled={variantId === null || maxQuantity === 0}
      >
        カートに入れる
      </button>

      {error && <p>{error}</p>}
    </div>
  );
}
