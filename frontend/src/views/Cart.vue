<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCartStore } from '@/stores/cartStore'
import type { CartLine } from '@/types'

const cartStore = useCartStore()
const email = ref('')
const name = ref('')
const syncing = ref(false)
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null)

const isEmpty = computed(() => cartStore.items.length === 0)
const total = computed(() => cartStore.total)

async function syncWithOdoo() {
  message.value = null
  syncing.value = true
  try {
    const res = await cartStore.syncWithBackend(
      email.value || undefined,
      name.value || undefined
    )
    message.value = {
      type: res.success ? 'success' : 'error',
      text: res.message + (res.order_name ? ` (${res.order_name})` : ''),
    }
    if (res.success) cartStore.clear()
  } catch (e) {
    message.value = {
      type: 'error',
      text: e instanceof Error ? e.message : 'Error al sincronizar',
    }
  } finally {
    syncing.value = false
  }
}

function remove(line: CartLine) {
  cartStore.removeItem(line.product_id)
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Carrito</h1>

    <div v-if="isEmpty" class="rounded-xl bg-surface-gray border border-surface-border p-12 text-center text-gray-500">
      No hay productos en el carrito.
      <router-link to="/" class="text-accent hover:underline ml-1">Ir a productos</router-link>
    </div>

    <template v-else>
      <div v-if="message" :class="[
        'mb-6 p-4 rounded-lg',
        message.type === 'success' ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'
      ]">
        {{ message.text }}
      </div>

      <div class="space-y-4 mb-8">
        <div
          v-for="line in cartStore.items"
          :key="line.product_id"
          class="flex items-center justify-between gap-4 p-4 bg-surface-white rounded-xl border border-surface-border"
        >
          <div>
            <span class="font-medium">{{ line.name ?? `Producto #${line.product_id}` }}</span>
            <span class="text-gray-500 text-sm ml-2">x {{ line.quantity }}</span>
          </div>
          <div class="flex items-center gap-4">
            <span class="font-semibold text-accent-dark">$ {{ (line.quantity * line.price_unit).toFixed(2) }} MXN</span>
            <button
              type="button"
              class="text-red-600 hover:text-red-700 text-sm"
              @click="remove(line)"
            >
              Quitar
            </button>
          </div>
        </div>
      </div>

      <div class="max-w-md space-y-4 p-6 bg-surface-white rounded-xl border border-surface-border">
        <p class="text-lg font-bold">Total: $ {{ total.toFixed(2) }} MXN</p>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nombre (opcional)</label>
          <input v-model="name" type="text" placeholder="Cliente Web" class="w-full px-4 py-2 rounded-lg border border-surface-border" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email (opcional)</label>
          <input v-model="email" type="email" placeholder="cliente@ejemplo.com" class="w-full px-4 py-2 rounded-lg border border-surface-border" />
        </div>
        <button
          type="button"
          class="w-full px-4 py-3 rounded-lg bg-accent text-white font-medium hover:bg-accent-dark disabled:opacity-50 transition-colors"
          :disabled="syncing"
          @click="syncWithOdoo"
        >
          {{ syncing ? 'Enviando...' : 'Crear presupuesto en Odoo' }}
        </button>
      </div>
    </template>
  </div>
</template>
