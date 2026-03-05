<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-b from-surface-muted/50 to-surface-gray">
    <Navbar />
    <main class="flex-1 container mx-auto px-4 sm:px-6 py-8 sm:py-10 max-w-7xl">
      <RouterView />
    </main>
  </div>
</template>
