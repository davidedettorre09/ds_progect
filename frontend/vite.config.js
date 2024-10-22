import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env.REACT_APP_BASE_API_URL_USER': JSON.stringify(env.REACT_APP_BASE_API_URL_USER),
      'process.env.REACT_APP_BASE_API_URL_DEVICE': JSON.stringify(env.REACT_APP_BASE_API_URL_DEVICE)
    },
    plugins: [react()],
    build: {
      rollupOptions: {
        output: {
          manualChunks: undefined
        }
      }
    },
    server: {
      historyApiFallback: true
    }
  }
})