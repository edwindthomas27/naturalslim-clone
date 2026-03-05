/**
 * Tipos compartidos entre API Odoo y frontend.
 */

export interface Product {
  id: number
  name: string
  list_price: number
  /** URL de la imagen en el backend (ej. /api/product/1/image). Null si no tiene imagen. */
  image_url: string | null
  description_sale: string
  category: string
  stock: number
}

export interface CartLine {
  product_id: number
  name?: string
  quantity: number
  price_unit: number
}

export interface CartSyncPayload {
  lines: CartLine[]
  partner_email?: string
  partner_name?: string
}

export interface CartSyncResponse {
  success: boolean
  message: string
  order_id: number | null
  order_name?: string
}

export interface ProductsApiResponse {
  products: Product[]
}
