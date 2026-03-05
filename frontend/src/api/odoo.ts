import type { ProductsApiResponse, CartSyncPayload, CartSyncResponse } from '@/types'

/** Base URL de la API Odoo. En dev es '' para usar el proxy de Vite. */
export function getBaseUrl(): string {
  if (import.meta.env.DEV) return ''
  return import.meta.env.VITE_ODOO_API_URL ?? 'http://localhost:8069'
}

export async function fetchProducts(): Promise<ProductsApiResponse> {
  const url = `${getBaseUrl()}/api/products`
  const res = await fetch(url, {
    method: 'GET',
    headers: { Accept: 'application/json' },
  })
  if (!res.ok) {
    throw new Error(`Error al cargar productos: ${res.status}`)
  }
  return res.json()
}

export async function syncCart(payload: CartSyncPayload): Promise<CartSyncResponse> {
  const res = await fetch(`${getBaseUrl()}/api/cart/sync`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(payload),
  })
  const data: CartSyncResponse = await res.json()
  if (!res.ok) {
    throw new Error(data.message ?? 'Error al sincronizar carrito')
  }
  return data
}
