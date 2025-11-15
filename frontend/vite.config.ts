import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
  resolve: {
    alias: {
      '@components': resolve(dirname(fileURLToPath(import.meta.url)), 'src/components'),
      '@pages': resolve(dirname(fileURLToPath(import.meta.url)), 'src/pages'),
      '@api': resolve(dirname(fileURLToPath(import.meta.url)), 'src/api'),
    },
  },
})
