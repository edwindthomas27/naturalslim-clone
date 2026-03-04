import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Home from '@/views/Home.vue'
import Cart from '@/views/Cart.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: 'Inicio - NaturalSlim' },
  },
  {
    path: '/cart',
    name: 'cart',
    component: Cart,
    meta: { title: 'Carrito - NaturalSlim' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const title = to.meta?.title as string | undefined
  document.title = title ?? 'NaturalSlim - Tienda'
  next()
})

export default router
