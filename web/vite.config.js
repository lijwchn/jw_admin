import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path' // 使用 import 语句引入 path 模块

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // 将路径改成别名@
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'), // 使用 resolve 函数而不是 path.resolve
    },
  },
  // css: {
  //   preprocessorOptions: {
  //     scss: {
  //       additionalData: `@import '@/assets/style/base.scss';`,
  //     },
  //   },
  // },
})
