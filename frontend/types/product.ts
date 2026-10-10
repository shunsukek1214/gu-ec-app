//FastAPIからのレスポンスを受けるための型定義
//例えばFastAPIのproduct_id: intをNext.jsでproduct_id: number;として受ける

export type ProductColor = {
  color_id: number;
  color_code: string;
  color_name: string;
};

export type ProductListItem = {
  product_id: number;
  name: string;
  price: string | number;
  image_url: string | null;
  colors: ProductColor[];
  in_stock: boolean;
};

export type ProductListResponse = {
  products: ProductListItem[];
};

export type ProductVariant = {
  variant_id: number;
  color_id: number;
  color_name: string;
  size_id: number;
  size_name: string;
  stock_quantity: number;
};

export type ProductImage = {
  image_id: number;
  color_id: number | null;
  image_url: string;
  display_order: number;
};

export type ProductDetailResponse = {
  product_id: number;
  name: string;
  price: string | number;
  description: string | null;
  colors: ProductColor[];
  variants: ProductVariant[];
  images: ProductImage[];
};
