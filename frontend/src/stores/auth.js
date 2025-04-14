import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {

  // 用户信息
  const user = ref(null)
  // 令牌
  const token = ref(localStorage.getItem('token') || null)
  
  // 判断用户是否已登录
  const isAuthenticated = computed(() => !!token.value)
  
  // 设置令牌
  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      setAuthHeader(newToken)
    } else {
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
  
  function setUser(userData) {
    user.value = userData
  }
  
  async function login(credentials) {
    try {
      console.log('发送登录请求:', credentials)
      const response = await axios.post('/api/auth/login', credentials)
      console.log('登录响应:', response.data)
      
      if (response.data && response.data.access_token) {
        setToken(response.data.access_token)
        setUser(response.data.user)
        return response.data
      } else {
        throw new Error('无效的响应格式：缺少access_token')
      }
    } catch (error) {
      console.error('登录失败详情:', error)
      if (error.response) {
        console.error('服务器响应状态:', error.response.status)
        console.error('服务器响应数据:', error.response.data)
      }
      throw error
    }
  }
  
  async function register(userData) {
    try {
      const response = await axios.post('/api/auth/register', userData)
      setToken(response.data.access_token)
      setUser(response.data.user)
      return response.data
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }
  
  async function logout() {
    setToken(null)
    setUser(null)
  }
  
  async function checkAuth() {
    if (!token.value) return false
    
    try {
      const response = await axios.get('/api/auth/me')
      setUser(response.data.user)
      return true
    } catch (error) {
      console.error('Authentication check failed:', error)
      setToken(null)
      setUser(null)
      return false
    }
  }
  
  // 如果令牌存在的话初始化认证头
  function setAuthHeader(authToken) {
    if (authToken) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`
      console.log('设置了Authorization头:', `Bearer ${authToken}`)
    } else {
      delete axios.defaults.headers.common['Authorization']
      console.log('删除了Authorization头')
    }
  }
  
  if (token.value) {
    setAuthHeader(token.value)
  }
  
  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth,
    setToken,
    setUser
  }
}) 