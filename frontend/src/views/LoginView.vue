<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="title">动态表格管理系统</h2>
      
      <el-form 
        ref="loginFormRef" 
        :model="loginForm" 
        :rules="rules" 
        label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            prefix-icon="User" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            @click="handleLogin" 
            :loading="loading"
            class="login-button">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-link">
        <span>没有账号？</span>
        <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 30, message: '密码长度在 6 到 30 个字符', trigger: 'blur' }
  ]
}

const loginFormRef = ref(null)

async function handleLogin() {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    
    loading.value = true
    console.log('开始登录请求，用户名:', loginForm.username)
    
    const response = await authStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    console.log('登录请求完成，响应:', response)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    console.error('登录处理错误:', error)
    
    // 根据错误类型显示不同的提示信息
    if (error.response) {
      const status = error.response.status
      const responseData = error.response.data
      
      if (status === 401) {
        ElMessage.error(responseData.message || '用户名或密码错误')
      } else if (status === 500) {
        ElMessage.error('服务器内部错误，请联系管理员')
        console.error('服务器错误详情:', responseData)
      } else {
        ElMessage.error(responseData.message || '登录失败')
      }
    } else if (error.request) {
      ElMessage.error('无法连接到服务器，请检查网络连接')
    } else {
      ElMessage.error('登录失败，请检查用户名和密码')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
  
  .login-box {
    width: 400px;
    padding: 40px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    
    .title {
      text-align: center;
      margin-bottom: 30px;
      color: var(--primary-color);
    }
    
    .login-button {
      width: 100%;
    }
    
    .register-link {
      text-align: center;
      margin-top: 16px;
      font-size: 14px;
      color: #606266;
      
      a {
        color: var(--primary-color);
        text-decoration: none;
        
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}
</style> 