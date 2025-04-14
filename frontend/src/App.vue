<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  // Check if token exists and try to refresh user data
  if (authStore.token) {
    try {
      await authStore.checkAuth()
      // If initial route is login, redirect to home
      if (router.currentRoute.value.name === 'login') {
        router.push({ name: 'dashboard' })
      }
    } catch (error) {
      console.error('Authentication failed:', error)
      // 如果认证失败，确保用户被导向登录页
      if (router.currentRoute.value.meta.requiresAuth !== false) {
        router.push({ name: 'login' })
      }
    }
  } else {
    // 如果没有token且当前页面需要认证，重定向到登录页
    if (router.currentRoute.value.meta.requiresAuth !== false) {
      router.push({ name: 'login' })
    }
  }
})
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.app-container {
  height: 100vh;
  width: 100vw;
}
</style> 