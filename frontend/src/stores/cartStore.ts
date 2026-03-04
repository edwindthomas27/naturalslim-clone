import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CartLine, Product } from '@/types'
import { syncCart } from '@/api/odoo'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartLine[]>([])

  const count = computed(() =>
    items.value.reduce((acc, line) => acc + line.quantity, 0)
  )

  const total = computed(() =>
    items.value.reduce((acc, line) => acc + line.quantity * line.price_unit, 0)
  )

  function addItem(product: Product, quantity: number = 1) {
    const existing = items.value.find((i) => i.product_id === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      items.value.push({
        product_id: product.id,
        name: product.name,
        quantity,
        price_unit: product.list_price,
      })
    }
  }

  function removeItem(productId: number) {
    items.value = items.value.filter((i) => i.product_id !== productId)
  }

  function setQuantity(productId: number, quantity: number) {
    const line = items.value.find((i) => i.product_id === productId)
    if (line) {
      if (quantity <= 0) {
        removeItem(productId)
      } else {
        line.quantity = quantity
      }
    }
  }

  function clear() {
    items.value = []
  }

  async function syncWithBackend(partnerEmail?: string, partnerName?: string) {
    const payload = {
      lines: items.value.map(({ product_id, quantity, price_unit }) => ({
        product_id,
        quantity,
        price_unit,
      })),
      partner_email: partnerEmail,
      partner_name: partnerName,
    }
    return syncCart(payload)
  }

  return {
    items,
    count,
    total,
    addItem,
    removeItem,
    setQuantity,
    clear,
    syncWithBackend,
  }
})
