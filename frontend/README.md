# 动态表格管理系统 - 前端

这是动态表格管理系统的前端部分，基于Vue 3和Element Plus构建。

## 环境要求

- Node.js 14+
- npm 6+ 或 yarn 1.22+

## 安装依赖

```bash
npm install
# 或
yarn install
```

## 开发模式

在开发模式下，系统提供热重载和开发服务器功能。

### 运行开发服务器

```bash
npm run dev
# 或
yarn dev
```

开发服务器将运行在 http://localhost:5173（或修改为其他可用端口）

### 开发模式配置

开发模式下，API请求会自动被代理到后端服务器（默认为http://localhost:5000）。
这个配置在 `vite.config.js`文件中设置：

```js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false
    }
  }
}
```

## 项目结构

```
frontend/
├── public/             # 静态资源
├── src/
│   ├── assets/         # 样式和图片等资源
│   ├── components/     # 可复用组件
│   ├── layouts/        # 布局组件
│   ├── router/         # 路由配置
│   ├── stores/         # Pinia状态管理
│   ├── views/          # 页面视图
│   │   ├── settings/   # 设置相关页面
│   │   └── tables/     # 表格相关页面
│   ├── App.vue         # 根组件
│   └── main.js         # 入口文件
├── .env.development    # 开发环境配置
├── .env.production     # 生产环境配置
├── index.html          # HTML模板
├── package.json        # 项目依赖
└── vite.config.js      # Vite配置
```

## 功能列表

- 用户认证（登录/注册）
- 动态表格管理
  - 创建新表格（自定义字段和类型）
  - 查看所有表格
  - 删除表格
- 动态表格数据管理
  - 查看表格数据
  - 添加新记录
  - 编辑现有记录
  - 删除记录
- 响应式布局，适配不同设备

## 技术栈

- Vue 3 (组合式API)
- Vite (构建工具)
- Vue Router (路由管理)
- Pinia (状态管理)
- Element Plus (UI组件库)
- Axios (HTTP客户端)

## 浏览器兼容性

支持所有现代浏览器（Chrome、Firefox、Safari、Edge等）的最新版本。不支持IE浏览器。

## 功能特性

### 用户认证

- 用户登录和注册
- JWT 认证

### 动态菜单

- 从后端动态加载菜单项
- 支持创建新表格后动态添加菜单项

### 表格管理

- 创建和删除表格
- 定义表格字段和字段类型
- 查看表格详情

### 动态表格数据操作

- 添加、编辑、删除表格数据
- 分页显示表格数据
- 搜索筛选数据

## 页面视图

- **登录/注册页** - 用户认证
- **首页** - 系统概览和快速导航
- **表格管理** - 创建和管理动态表格
- **动态表格页** - 操作动态创建的表格数据

## 开发须知

- 前端使用代理配置连接到后端 API，确保后端服务在 `http://localhost:5000` 运行
- 默认使用管理员账户登录：
  - 用户名: admin
  - 密码: admin123
