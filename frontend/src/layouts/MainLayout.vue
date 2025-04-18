<template>
  <div class="main-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="logo-container">
        <h2>后台管理系统</h2>
      </div>
      
      <el-menu 
        router 
        :default-active="activeRoute" 
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF">
        <template v-for="item in menuItems" :key="item.name">
          <!-- No children -->
          <el-menu-item v-if="!item.children || item.children.length === 0" :index="item.path">
            <el-icon><component :is="getIconComponent(item.icon)" /></el-icon>
            <span>{{ item.display_name }}</span>
          </el-menu-item>
          
          <!-- With children -->
          <el-sub-menu v-else :index="item.name">
            <template #title>
              <el-icon><component :is="getIconComponent(item.icon)" /></el-icon>
              <span>{{ item.display_name }}</span>
            </template>
            
            <el-menu-item 
              v-for="child in item.children" 
              :key="child.name" 
              :index="child.path">
              <el-icon><component :is="getIconComponent(child.icon)" /></el-icon>
              <span>{{ child.display_name }}</span>
            </el-menu-item>
          </el-sub-menu>
        </template>
      </el-menu>
    </div>
    
    <!-- Main content area -->
    <div class="main-content">
      <!-- Header -->
      <div class="header">
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentRoute.meta.title">
              {{ currentRoute.meta.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="header-right">
          <el-button type="primary" size="small" class="go-button" @click="goToFrontend">
            代码生成
          </el-button>

          <div class="user-info">
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="user-dropdown-link">
                {{ user?.username || '用户' }}
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>
      
      <!-- Page content -->
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMenuStore } from '@/stores/menu'
import { 
  Setting, Grid, Document, Menu as MenuIcon, 
  HomeFilled, ArrowDown, Edit
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const menuStore = useMenuStore()

// Refs and computed properties
const user = computed(() => authStore.user)
const menuItems = computed(() => menuStore.menuItems)
const activeRoute = computed(() => route.path)
const currentRoute = computed(() => route)

// Load menu items
onMounted(async () => {
  if (!menuStore.menuLoaded) {
    await menuStore.fetchMenu()
  }
})

// Map icon names to components
function getIconComponent(iconName) {
  const iconMap = {
    'settings': Setting,
    'table': Grid,
    'grid': Grid,
    'edit': Edit,
    'menu': MenuIcon,
    'document': Document,
    'home': HomeFilled
  }
  return iconMap[iconName] || Document
}

// Dropdown command handler
function handleCommand(command) {
  if (command === 'logout') {
    authStore.logout()
    router.push('/login')
  } else if (command === 'profile') {
    // Profile functionality not implemented in this version
    console.log('Profile clicked')
  }
}

function goToFrontend() {
  window.open('http://localhost:5174/', '_blank')
}


</script>

<style lang="scss" scoped>
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.go-button {
  margin-right: 0;
}



.main-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  
  .sidebar {
    width: var(--sidebar-width);
    background-color: #304156;
    display: flex;
    flex-direction: column;
    color: white;
    height: 100%;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    z-index: 2;
    
    .logo-container {
      height: var(--header-height);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 16px;
      
      h2 {
        color: #fff;
        font-size: 18px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
    
    .sidebar-menu {
      flex: 1;
      border-right: none;
      width: 100%;
    }
  }
  
  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    
    .header {
      height: var(--header-height);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      background-color: #fff;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
      z-index: 1;
      
      .breadcrumb {
        display: flex;
        align-items: center;
      }
      
      .user-info {
        .user-dropdown-link {
          cursor: pointer;
          display: flex;
          align-items: center;
          
          .el-icon {
            margin-left: 8px;
          }
        }
      }
    }
    
    .content {
      flex: 1;
      padding: 20px;
      overflow: auto;
      background-color: #f0f2f5;
    }
  }
}
</style> 