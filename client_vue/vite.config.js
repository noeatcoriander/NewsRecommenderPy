/**
 * vite构建工具的核心配置文件
 * 创建vue3前端系统时，自动生成当前文件
 * 主要用于构建、编译和运行vue3前端系统、创建vue3前端服务器、设置服务器的端口号、配置代理等
 */
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

//vite配置选项
export default defineConfig({
  //服务器配置
  server: {
    host: '0.0.0.0', //允许外部访问前端系统，默认只可本地访问：localhost或127.0.0.1
    port: 5173, //端口号，默认5173
    open: false, //启动后是否自动打开浏览器
    //检查端口是否被占用，默认false
    //如果为true，5173端口号被占用时运行直接抛出异常，如果为false，vite会使用新的端口号5174运行
    strictPort: false,
    allowedHosts: true //允许所有主机访问
  },
  //插件配置
  plugins: [
    vue() //启用Vue3的单文件组件（SFC）支持，主要用于解析.vue文件，默认配置
  ],
  //解析配置
  resolve: {
    //路径别名配置
    alias: {
      //使用@符号指向src路径，即"@/"表示vue3前端系统的src文件夹，可在vue、js、css等文件中使用
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
