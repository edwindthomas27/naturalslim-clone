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
  <div class="animate-fade-in">
    <!-- Hero -->
    <section class="mb-10 sm:mb-12">
      <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 tracking-tight mb-2">
        Nuestra tienda
      </h1>
      <p class="text-gray-600 text-lg max-w-xl">
        Descubre productos NaturalSlim para tu bienestar. Envíos a todo México.
      </p>
    </section>

    <!-- Loading skeletons -->
    <div v-if="loading" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div
        v-for="i in 8"
        :key="i"
        class="bg-white rounded-2xl border border-surface-border overflow-hidden shadow-card"
      >
        <div class="aspect-square bg-surface-muted animate-pulse" />
        <div class="p-5 space-y-3">
          <div class="h-5 bg-surface-muted rounded-lg animate-pulse w-3/4" />
          <div class="h-4 bg-surface-muted rounded animate-pulse w-1/2" />
          <div class="flex justify-between items-center pt-2">
            <div class="h-6 bg-surface-muted rounded w-20 animate-pulse" />
            <div class="h-10 bg-surface-muted rounded-xl w-24 animate-pulse" />
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div
      v-else-if="error"
      class="rounded-2xl bg-red-50/90 border border-red-200 p-6 sm:p-8 text-red-700 shadow-inner-soft"
    >
      <p class="font-medium">No se pudieron cargar los productos</p>
      <p class="mt-2 text-sm opacity-90">{{ error }}</p>
    </div>

    <!-- Product grid -->
    <template v-else>
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <ProductCard
          v-for="product in filteredProducts"
          :key="product.id"
          :product="product"
        />
      </div>
      <div
        v-if="filteredProducts.length === 0"
        class="rounded-2xl bg-surface-muted/80 border border-surface-border p-12 sm:p-16 text-center"
      >
        <p class="text-gray-500 text-lg">
          No hay productos que coincidan con tu búsqueda.
        </p>
        <p class="text-gray-400 text-sm mt-1">Prueba con otras palabras.</p>
      </div>
    </template>
  </div>
</template>
