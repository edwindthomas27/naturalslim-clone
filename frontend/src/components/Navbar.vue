<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useCartStore } from '@/stores/cartStore'
import { useSearchStore } from '@/stores/searchStore'

const cartStore = useCartStore()
const searchStore = useSearchStore()
const searchQuery = ref(searchStore.query)

watch(searchQuery, (v) => searchStore.setQuery(v))
watch(() => searchStore.query, (v) => { searchQuery.value = v })

const cartCount = computed(() => cartStore.count)

function onSearch() {
  searchStore.setQuery(searchQuery.value)
}
</script>

<template>
  <header class="bg-white/95 backdrop-blur-md border-b border-surface-border/80 shadow-card sticky top-0 z-50">
    <div class="container mx-auto px-4 sm:px-6 max-w-7xl">
      <div class="flex items-center justify-between h-16 sm:h-18 gap-4">
        <router-link
          to="/"
          class="flex items-center gap-2 shrink-0 transition-opacity hover:opacity-90"
        >
          <img src="/logo-nS2.svg" alt="NaturalSlim" class="h-10 sm:h-11 w-auto" />
        </router-link>

        <div class="flex-1 max-w-xl hidden sm:block mx-6">
          <form @submit.prevent="onSearch" class="relative">
            <span class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input
              v-model="searchQuery"
              type="search"
              placeholder="Buscar productos..."
              class="w-full pl-11 pr-4 py-2.5 rounded-xl border border-surface-border bg-surface-muted/80 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent/30 focus:border-accent transition-shadow"
            />
          </form>
        </div>

        <div class="flex items-center gap-1 sm:gap-2">
          <router-link
            to="/cart"
            class="relative p-2.5 sm:p-3 rounded-xl text-gray-600 hover:bg-surface-muted hover:text-accent-dark transition-all duration-200"
            title="Ver carrito"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 sm:h-7 sm:w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <span
              v-if="cartCount > 0"
              class="absolute top-0.5 right-0.5 min-w-[1.25rem] h-5 px-1.5 flex items-center justify-center text-xs font-bold text-white bg-accent rounded-full shadow-sm"
            >
              {{ cartCount > 99 ? '99+' : cartCount }}
            </span>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>
