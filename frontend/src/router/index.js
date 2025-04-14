import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMenuStore } from '@/stores/menu'

// 静态布局导入
import MainLayout from '@/layouts/MainLayout.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'
import TableManagementView from '@/views/settings/TableManagementView.vue'
import NotFoundView from '@/views/NotFoundView.vue'

// 默认路由
const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: DashboardView,
        meta: { title: '首页' }
      },
      {
        path: 'settings/table-management',
        name: 'table-management',
        component: TableManagementView,
        meta: { title: '表格管理' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 导航守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const menuStore = useMenuStore()
  
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  // 如果路由需要认证但用户未登录，重定向到登录页
  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
    return
  }
  
  // 如果已登录且访问登录/注册页，重定向到首页
  if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'dashboard' })
    return
  }
  
  // 继续访问请求的路由
  next()
})

// 添加动态表格路由
export function addDynamicTableRoutes() {
  const menuStore = useMenuStore()
  const tables = menuStore.tableMenuItems
  
  console.log('开始添加动态表格路由，数量:', tables.length)
  
  try {
    // 遍历每个表格
    tables.forEach(table => {
      // 从表名中提取实际表名（移除'table-'前缀）
      const actualTableName = table.name.replace('table-', '')
      
      // 路由名称和路径
      const routeName = table.name
      const routePath = `/tables/${actualTableName}`  // 注意：这是绝对路径
      
      // 检查路由是否已经存在
      const existingRoute = router.getRoutes().find(r => 
        r.name === routeName || 
        r.path === routePath
      )
      
      if (existingRoute) {
        console.log(`路由已存在，跳过: ${routePath}`)
        return
      }
      
      // 添加路由到根路由
      router.addRoute({
        path: routePath,
        name: routeName,
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
          {
            path: '',  // 默认子路由
            component: () => import('@/views/tables/DynamicTableView.vue'),
            props: { tableName: actualTableName },
            meta: { 
              title: table.display_name,
              dynamicTable: true
            }
          }
        ]
      })
      
      console.log(`成功添加动态表格路由: ${routePath}, 名称: ${routeName}`)
    })
  } catch (error) {
    console.error('动态路由添加失败:', error)
  }
}

export default router 