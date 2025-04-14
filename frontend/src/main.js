import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import './assets/styles/main.scss'
import axios from 'axios'

// 环境变量
const isDebugMode = import.meta.env.VITE_APP_DEBUG === 'true'
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

// 设置axios默认配置
axios.defaults.baseURL = apiBaseUrl || '/api'

// 添加axios请求拦截器
axios.interceptors.request.use(config => {
  // 从localStorage获取token
  const token = localStorage.getItem('token')
  // 如果token存在，添加到请求头
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    if (isDebugMode) {
      console.log(`发送请求到 ${config.url}，已添加Authorization头:`, config.headers.Authorization)
    }
  } else if (isDebugMode) {
    console.log(`发送请求到 ${config.url}，未找到token`)
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 添加axios响应拦截器
axios.interceptors.response.use(response => {
  return response
}, error => {
  // 如果收到401响应，可能是token失效或未授权
  if (error.response && error.response.status === 401) {
    if (isDebugMode) {
      console.error('认证失败:', error.response.status)
    }
    // 清除token
    localStorage.removeItem('token')
    // 重定向到登录页
    router.push('/login')
  }
  // 对于422错误，只记录日志但不自动登出
  else if (isDebugMode && error.response && error.response.status === 422) {
    console.warn('请求参数验证失败:', error.response.status)
  }
  return Promise.reject(error)
})

// 创建Vue应用
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// 添加全局日志函数
app.config.globalProperties.$log = (...args) => {
  if (isDebugMode) {
    console.log(...args)
  }
}

app.mount('#app') 