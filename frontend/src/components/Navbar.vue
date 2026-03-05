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
  <header class="bg-surface-white border-b border-surface-border shadow-sm sticky top-0 z-50">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16 gap-4">
        <router-link to="/" class="flex items-center gap-2 shrink-0">
          <img src="/logo-nS2.svg" alt="NaturalSlim" class="h-11 w-auto" />
        </router-link>

        <div class="flex-1 max-w-md hidden sm:block">
          <form @submit.prevent="onSearch" class="flex gap-2">
            <input
              v-model="searchQuery"
              type="search"
              placeholder="Buscar productos..."
              class="w-full px-4 py-2 rounded-lg border border-surface-border bg-surface-gray focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent"
            />
            <button
              type="submit"
              class="px-4 py-2 rounded-lg bg-accent text-white font-medium hover:bg-accent-dark transition-colors"
            >
              Buscar
            </button>
          </form>
        </div>

        <div class="flex items-center gap-4">
          <router-link
            to="/cart"
            class="p-2 rounded-lg text-gray-600 hover:bg-surface-gray hover:text-accent-dark transition-colors"
            title="Carrito"
          >
            <span class="relative inline-flex items-center gap-1">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
              <span
                v-if="cartCount > 0"
                class="absolute -top-1 -right-1 min-w-[1.25rem] h-5 px-1 flex items-center justify-center text-xs font-bold text-white bg-accent rounded-full"
              >
                {{ cartCount > 99 ? '99+' : cartCount }}
              </span>
            </span>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>
