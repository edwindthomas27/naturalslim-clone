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
  if (imageError.value) return null
  if (props.product.image_url) {
    return getBaseUrl() + props.product.image_url
  }
  return null
})

function onImageError() {
  if (import.meta.env.DEV) {
    console.warn('[ProductCard] Imagen no cargó:', props.product.id, props.product.name)
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
    class="group bg-white rounded-2xl border border-surface-border overflow-hidden shadow-card hover:shadow-card-hover hover:border-accent/20 transition-all duration-300 flex flex-col animate-slide-up"
  >
    <div class="aspect-square bg-surface-muted relative overflow-hidden">
      <img
        v-if="imageSrc"
        :src="imageSrc"
        :alt="product.name"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
        loading="lazy"
      />
      <div
        v-else
        class="w-full h-full flex items-center justify-center text-gray-300"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-20 w-20"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6 6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
      </div>
      <span
        v-if="product.category"
        class="absolute top-3 left-3 px-2.5 py-1 text-xs font-semibold rounded-lg bg-accent text-white shadow-sm"
      >
        {{ product.category }}
      </span>
    </div>

    <div class="p-5 flex flex-col flex-1">
      <h3 class="font-semibold text-gray-900 line-clamp-2 mb-2 leading-snug">
        {{ product.name }}
      </h3>
      <p
        v-if="product.description_sale"
        class="text-sm text-gray-500 line-clamp-2 mb-4 flex-1 min-h-[2.5rem]"
      >
        {{ product.description_sale }}
      </p>
      <div class="flex items-end justify-between mt-auto gap-3">
        <div>
          <span class="text-xl font-bold text-accent-dark">
            $ {{ product.list_price.toFixed(2) }}
          </span>
          <span class="text-sm text-gray-500 ml-0.5">MXN</span>
        </div>
        <button
          type="button"
          class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-accent text-white font-semibold text-sm hover:bg-accent-dark active:scale-[0.98] transition-all duration-200 shadow-sm shrink-0"
          @click="addToCart"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Agregar
        </button>
      </div>
      <p v-if="product.stock !== undefined" class="text-xs text-gray-400 mt-2">
        Stock disponible: {{ product.stock }}
      </p>
    </div>
  </article>
</template>
