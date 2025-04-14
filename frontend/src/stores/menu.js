import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { addDynamicTableRoutes } from '@/router'

export const useMenuStore = defineStore('menu', () => {
  // 状态
  const menuItems = ref([])
  const menuLoaded = ref(false)
  
  // 计算属性
  const tableMenuItems = computed(() => {
    // 查找 "tables" 菜单
    const tablesMenu = menuItems.value.find(item => item.name === 'tables')
    // 返回其子菜单或空数组（如果未找到）
    return tablesMenu?.children || []
  })
  
  // 操作
  async function fetchMenu() {
    try {
      const response = await axios.get('/api/debug/menu')
      if (response.data.status === 'success') {
        menuItems.value = response.data.menu
        menuLoaded.value = true
        
        // 为表格添加动态路由
        addDynamicTableRoutes()
      }
      return menuItems.value
    } catch (error) {
      console.error('获取菜单失败:', error)
      return []
    }
  }
  
  function addTableMenuItem(tableItem) {
    // 查找 "tables" 菜单
    const tablesMenu = menuItems.value.find(item => item.name === 'tables')
    
    if (tablesMenu) {
      // 如果子菜单数组不存在则初始化
      if (!tablesMenu.children) {
        tablesMenu.children = []
      }
      
      // 确保路径始终以斜杠开头
      if (tableItem.path && !tableItem.path.startsWith('/')) {
        tableItem.path = '/' + tableItem.path
      }
      
      // 检查是否已存在相同名称的菜单项
      const existingItemIndex = tablesMenu.children.findIndex(
        item => item.name === tableItem.name
      )
      
      // 如果已存在则更新它
      if (existingItemIndex !== -1) {
        console.log(`更新已存在的菜单项: ${tableItem.name}`)
        tablesMenu.children[existingItemIndex] = tableItem
      } else {
        // 否则添加新的菜单项
        console.log(`添加新菜单项: ${tableItem.name}, 路径: ${tableItem.path}`)
        tablesMenu.children.push(tableItem)
      }
      
      // 延迟添加动态路由，确保菜单项先处理完毕
      setTimeout(() => {
        addDynamicTableRoutes()
      }, 100)
    } else {
      console.error('未找到 "tables" 菜单项，无法添加子菜单')
    }
  }
  
  return {
    menuItems,
    menuLoaded,
    tableMenuItems,
    fetchMenu,
    addTableMenuItem
  }
})