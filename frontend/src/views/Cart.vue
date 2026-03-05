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
  <div class="animate-fade-in">
    <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 tracking-tight mb-2">Carrito</h1>
    <p class="text-gray-600 mb-8">Revisa tu pedido y completa los datos para crear el presupuesto.</p>

    <div
      v-if="isEmpty"
      class="rounded-2xl bg-white border border-surface-border shadow-card p-12 sm:p-16 text-center"
    >
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-surface-muted text-gray-400 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
        </svg>
      </div>
      <p class="text-gray-500 text-lg">Tu carrito está vacío.</p>
      <router-link
        to="/"
        class="inline-flex items-center gap-2 mt-4 px-5 py-2.5 rounded-xl bg-accent text-white font-semibold text-sm hover:bg-accent-dark transition-colors"
      >
        Ver productos
      </router-link>
    </div>

    <template v-else>
      <div
        v-if="message"
        :class="[
          'mb-6 p-4 rounded-xl border',
          message.type === 'success'
            ? 'bg-green-50 text-green-800 border-green-200'
            : 'bg-red-50 text-red-700 border-red-200'
        ]"
      >
        {{ message.text }}
      </div>

      <div class="grid gap-6 lg:grid-cols-3 mb-8">
        <div class="lg:col-span-2 space-y-4">
          <div
            v-for="line in cartStore.items"
            :key="line.product_id"
            class="flex items-center justify-between gap-4 p-5 bg-white rounded-2xl border border-surface-border shadow-card"
          >
            <div class="min-w-0 flex-1">
              <span class="font-semibold text-gray-900">{{ line.name ?? `Producto #${line.product_id}` }}</span>
              <span class="text-gray-500 text-sm ml-2">× {{ line.quantity }}</span>
            </div>
            <div class="flex items-center gap-4 shrink-0">
              <span class="font-bold text-accent-dark">$ {{ (line.quantity * line.price_unit).toFixed(2) }} MXN</span>
              <button
                type="button"
                class="p-2 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                title="Quitar"
                @click="remove(line)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-1">
          <div class="sticky top-24 p-6 bg-white rounded-2xl border border-surface-border shadow-card">
            <p class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-1">Total</p>
            <p class="text-2xl font-bold text-gray-900 mb-6">$ {{ total.toFixed(2) }} MXN</p>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Nombre (opcional)</label>
                <input
                  v-model="name"
                  type="text"
                  placeholder="Tu nombre"
                  class="w-full px-4 py-2.5 rounded-xl border border-surface-border bg-surface-muted/50 focus:outline-none focus:ring-2 focus:ring-accent/30 focus:border-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Email (opcional)</label>
                <input
                  v-model="email"
                  type="email"
                  placeholder="tu@email.com"
                  class="w-full px-4 py-2.5 rounded-xl border border-surface-border bg-surface-muted/50 focus:outline-none focus:ring-2 focus:ring-accent/30 focus:border-accent"
                />
              </div>
            </div>

            <button
              type="button"
              class="w-full mt-6 px-4 py-3.5 rounded-xl bg-accent text-white font-semibold hover:bg-accent-dark disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
              :disabled="syncing"
              @click="syncWithOdoo"
            >
              <svg v-if="syncing" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ syncing ? 'Enviando...' : 'Crear presupuesto en Odoo' }}
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
