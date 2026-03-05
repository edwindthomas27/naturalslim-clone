import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5180,
    host: true,
    proxy: {
      // En desarrollo, las peticiones a /api se reenvían a Odoo.
      // En Docker usar VITE_PROXY_TARGET=http://odoo:8069 (nombre del servicio).
      // En local, por defecto http://localhost:8069
      '/api': {
        target: process.env.VITE_PROXY_TARGET || 'http://localhost:8069',
        changeOrigin: true,
      },
    },
  },
})
