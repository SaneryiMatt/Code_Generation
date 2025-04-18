// src/main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import hljs from 'highlight.js' // 代码高亮库
import router from './router'
// 初始化应用
const app = createApp(App)

// 添加Pinia状态管理
app.use(createPinia())

// 全局样式
import '@/assets/main.scss'

// 全局注册代码高亮指令
app.directive('highlight', {
  mounted(el) {
    hljs.highlightElement(el)
  },
  updated(el) {
    hljs.highlightElement(el)
  }
})
app.use(router)
// 挂载应用
app.mount('#app')
