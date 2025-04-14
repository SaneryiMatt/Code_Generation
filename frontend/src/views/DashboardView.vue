<template>
  <div class="dashboard-container page-container">
    <div class="page-header">
      <h1 class="page-title">系统首页</h1>
    </div>
    
    <div class="page-content">
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="welcome-card">
            <template #header>
              <div class="card-header">
                <h3>欢迎使用动态表格管理系统</h3>
              </div>
            </template>
            <div class="card-content">
              <p>本系统支持动态创建和管理数据表格，您可以通过以下方式开始使用：</p>
              <ol>
                <li>点击左侧菜单中的"设置" -> "表格管理"，创建一个新的数据表格</li>
                <li>在表格管理页面，定义您需要的字段和字段类型</li>
                <li>创建表格后，系统会在左侧"表格"菜单下添加对应的子菜单</li>
                <li>点击子菜单，进入对应的表格页面进行数据管理</li>
              </ol>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="mt-3">
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <h3>快速导航</h3>
              </div>
            </template>
            <div class="card-content">
              <el-button 
                type="primary" 
                @click="$router.push('/settings/table-management')">
                管理表格
              </el-button>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <h3>现有表格</h3>
              </div>
            </template>
            <div class="card-content">
              <el-empty v-if="!tableMenuItems.length" description="暂无表格，请先创建" />
              <div v-else class="table-list">
                <el-tag 
                  v-for="table in tableMenuItems" 
                  :key="table.name"
                  class="table-tag"
                  @click="navigateToTable(table)">
                  {{ table.display_name }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMenuStore } from '@/stores/menu'

const router = useRouter()
const menuStore = useMenuStore()

const tableMenuItems = computed(() => menuStore.tableMenuItems)

function navigateToTable(table) {
  router.push(table.path)
}
</script>

<style lang="scss" scoped>
.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  p {
    margin-bottom: 16px;
  }
  
  ol {
    padding-left: 20px;
    
    li {
      margin-bottom: 8px;
    }
  }
}

.table-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  
  .table-tag {
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
  }
}
</style> 