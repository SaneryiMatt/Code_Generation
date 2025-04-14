# 动态表格管理系统

基于 Flask + Vue 的动态表格管理系统，允许管理员通过管理界面动态创建新的数据表格，并在前端展示和操作这些表格数据。

## 项目特点

- 前后端分离架构
- 支持动态创建表格和字段
- 动态生成前端界面和路由
- 支持多种字段类型
- 用户登录和注册功能
- 数据库类型可在 MySQL 和 SQLite 之间切换

## 技术栈

### 前端
- Vue.js 3.x
- Vue Router 4.x
- Pinia (状态管理)
- Element Plus (UI组件库)
- Axios (HTTP客户端)

### 后端
- Python 3.x
- Flask 框架
- SQLAlchemy ORM
- JWT 认证
- 支持 MySQL 和 SQLite 数据库

## 项目结构

```
/
├── backend/              # 后端 Flask 应用
│   ├── models/           # 数据模型
│   ├── views/            # API 视图
│   ├── app.py            # 应用入口
│   ├── config.py         # 配置文件
│   └── commands.py       # 命令行工具
└── frontend/             # 前端 Vue 应用
    ├── src/              # 源代码
    │   ├── assets/       # 资源文件
    │   ├── components/   # 组件
    │   ├── layouts/      # 布局组件
    │   ├── router/       # 路由
    │   ├── stores/       # 状态管理
    │   ├── views/        # 页面视图
    │   ├── App.vue       # 根组件
    │   └── main.js       # 入口文件
    └── index.html        # HTML 模板
```

## 快速开始

### 后端

1. 进入后端目录
   ```bash
   cd backend
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置数据库类型和连接信息
   ```

4. 初始化数据库
   ```bash
   # 选择数据库类型 (sqlite 或 mysql)
   flask db-config sqlite  # 或 flask db-config mysql
   
   # 初始化数据库表结构
   flask db-init
   
   # 填充初始数据
   flask db-seed
   ```

5. 运行后端服务
   ```bash
   flask run  # 默认在 5000 端口
   ```

### 前端

1. 进入前端目录
   ```bash
   cd frontend
   ```

2. 安装依赖
   ```bash
   npm install
   ```

3. 运行开发服务器
   ```bash
   npm run dev
   ```

4. 构建生产版本
   ```bash
   npm run build
   ```

## 使用说明

1. 使用默认账户登录系统
   - 用户名：admin
   - 密码：admin123

2. 创建新表格
   - 从左侧导航栏点击"设置" -> "表格管理"
   - 点击"创建新表格"按钮
   - 填写表格名称、显示名称和描述
   - 添加所需的字段，设置字段类型和属性
   - 点击"创建表格"按钮提交

3. 使用新创建的表格
   - 表格创建成功后，会在左侧导航栏的"表格"菜单下添加新的子菜单
   - 点击对应的菜单项，进入该表格的数据管理页面
   - 可以在该页面添加、编辑和删除数据

## 字段类型支持

- 文本 (text) - 短文本
- 长文本 (longtext) - 多行文本
- 数字 (number) - 浮点数
- 整数 (integer) - 整数
- 日期 (date) - 日期选择器
- 日期时间 (datetime) - 日期和时间选择器
- 布尔值 (boolean) - 开关 