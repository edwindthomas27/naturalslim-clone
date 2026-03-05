<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Product } from '@/types'
import { useCartStore } from '@/stores/cartStore'
import { getBaseUrl } from '@/api/odoo'

const props = defineProps<{
  product: Product
}>()

const cartStore = useCartStore()
const imageError = ref(false)

const imageSrc = computed(() => {
  if (!props.product.image_url || imageError.value) return null
  return getBaseUrl() + props.product.image_url
})

function onImageError() {
  if (import.meta.env.DEV) {
    const url = getBaseUrl() + (props.product.image_url || '')
    console.warn('[ProductCard] Imagen no cargó:', props.product.id, props.product.name, { url })
  }
  imageError.value = true
}

watch(() => props.product.id, () => {
  imageError.value = false
})

function addToCart() {
  cartStore.addItem(props.product, 1)
}
</script>

<template>
  <article
    class="bg-surface-white rounded-xl border border-surface-border overflow-hidden shadow-sm hover:shadow-md transition-shadow flex flex-col"
  >
    <div class="aspect-square bg-surface-gray relative overflow-hidden">
      <img
        v-if="imageSrc"
        :src="imageSrc"
        :alt="product.name"
        class="w-full h-full object-cover"
        loading="lazy"
        @error="onImageError"
      />
      <div
        v-else
        class="w-full h-full flex items-center justify-center text-gray-400"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-16 w-16"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6 6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
      </div>
      <span
        v-if="product.category"
        class="absolute top-2 left-2 px-2 py-1 text-xs font-medium rounded-md bg-accent/90 text-white"
      >
        {{ product.category }}
      </span>
    </div>

    <div class="p-4 flex flex-col flex-1">
      <h3 class="font-semibold text-gray-900 line-clamp-2 mb-1">
        {{ product.name }}
      </h3>
      <p
        v-if="product.description_sale"
        class="text-sm text-gray-500 line-clamp-2 mb-3 flex-1"
      >
        {{ product.description_sale }}
      </p>
      <div class="flex items-center justify-between mt-auto gap-2">
        <span class="text-lg font-bold text-accent-dark">
          $ {{ product.list_price.toFixed(2) }} <span class="text-sm font-normal">MXN</span>
        </span>
        <button
          type="button"
          class="px-4 py-2 rounded-lg bg-accent text-white font-medium text-sm hover:bg-accent-dark transition-colors shrink-0"
          @click="addToCart"
        >
          Agregar
        </button>
      </div>
      <p v-if="product.stock !== undefined" class="text-xs text-gray-400 mt-1">
        Stock: {{ product.stock }}
      </p>
    </div>
  </article>
</template>
