<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import ProductCard from '@/components/ProductCard.vue'
import type { Product } from '@/types'
import { fetchProducts } from '@/api/odoo'
import { useSearchStore } from '@/stores/searchStore'

const searchStore = useSearchStore()
const products = ref<Product[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const filteredProducts = computed(() => {
  const q = searchStore.query.trim().toLowerCase()
  if (!q) return products.value
  return products.value.filter(
    (p) =>
      p.name.toLowerCase().includes(q) ||
      (p.category && p.category.toLowerCase().includes(q))
  )
})

onMounted(async () => {
  try {
    const data = await fetchProducts()
    products.value = data.products ?? []
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'Error al cargar productos'
    if (msg === 'Failed to fetch') {
      error.value = 'No se puede conectar con el backend. Comprueba que Odoo esté en marcha en http://localhost:8069 y que el módulo "NaturalSlim API" esté instalado.'
    } else {
      error.value = msg
    }
  } finally {
    loading.value = false
  }
})

</script>

<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-2">Productos</h1>
    <p class="text-gray-600 mb-8">
      Descubre nuestros productos NaturalSlim.
    </p>

    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div
        v-for="i in 8"
        :key="i"
        class="h-80 rounded-xl bg-surface-gray animate-pulse"
      />
    </div>

    <div v-else-if="error" class="rounded-xl bg-red-50 border border-red-200 p-6 text-red-700">
      {{ error }}
    </div>

    <template v-else>
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <ProductCard
          v-for="product in filteredProducts"
          :key="product.id"
          :product="product"
        />
      </div>
      <p
        v-if="filteredProducts.length === 0"
        class="text-center text-gray-500 py-12"
      >
        No hay productos que coincidan con tu búsqueda.
      </p>
    </template>
  </div>
</template>
