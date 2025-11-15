import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const r = (p) => resolve(dirname(fileURLToPath(import.meta.url)), p)

export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
  resolve: {
    alias: {
      '@components': r('src/components'),
      '@pages': r('src/pages'),
      '@api': r('src/api'),
    },
  },
})
