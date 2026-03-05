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
    // En Docker (y a veces en Windows) los cambios del host no disparan el watcher.
    // Con polling, Vite revisa los archivos cada X ms y aplica HMR.
    watch: {
      usePolling: true,
      interval: 500,
    },
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
