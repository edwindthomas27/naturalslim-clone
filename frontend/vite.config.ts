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
    port: 5173,
    host: true,
    proxy: {
      // En desarrollo, las peticiones a /api se reenvían a Odoo (evita CORS y errores de conexión)
      '/api': {
        target: 'http://localhost:8069',
        changeOrigin: true,
      },
    },
  },
})
