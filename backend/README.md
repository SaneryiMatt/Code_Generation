# 动态表格管理系统 - 后端

这是动态表格管理系统的后端API服务，基于Flask构建。

## 环境要求

- Python 3.7+
- SQLite（开发环境）或MySQL（生产环境）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 开发模式

在开发模式下，系统使用SQLite数据库，并提供调试功能。

### 环境变量设置

```bash
# 开发环境变量设置
export FLASK_ENV=development
export FLASK_DEBUG=1
export DATABASE_TYPE=sqlite
export SQLITE_DB_PATH=instance/dynamic_tables.db
```

Windows环境:

```powershell
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = 1
$env:DATABASE_TYPE = "sqlite"
$env:SQLITE_DB_PATH = "instance/dynamic_tables.db"
```

### 运行开发服务器

```bash
python app.py
```

开发服务器将运行在 http://127.0.0.1:5000


## 数据库初始化

首次运行前需要初始化数据库：

```bash
flask db-init
flask db-seed
```

此命令将创建必要的表格和初始菜单项。

## API端点

### 认证相关

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前登录用户信息

### 表格管理

- `GET /api/tables/` - 获取所有表格
- `GET /api/tables/<int:table_id>` - 获取特定表格
- `POST /api/tables/` - 创建新表格
- `DELETE /api/tables/<int:table_id>` - 删除表格

### 动态表格数据

- `GET /api/dynamic/<string:table_name>` - 获取表格数据
- `POST /api/dynamic/<string:table_name>` - 添加表格记录
- `GET /api/dynamic/<string:table_name>/<int:record_id>` - 获取特定记录
- `PUT /api/dynamic/<string:table_name>/<int:record_id>` - 更新记录
- `DELETE /api/dynamic/<string:table_name>/<int:record_id>` - 删除记录

### 调试接口

- `GET /api/debug/menu` - 获取菜单结构

## 项目结构

```
backend/
├── app.py               # 应用入口
├── config.py            # 配置文件
├── commands.py          # 命令行工具
├── requirements.txt     # 依赖列表
├── models/              # 数据模型
│   ├── __init__.py
│   ├── user.py
│   ├── table_definition.py
│   ├── field_definition.py
│   └── menu_item.py
└── views/               # API 视图
    ├── __init__.py
    ├── auth.py          # 认证相关
    ├── tables.py        # 表格定义管理
    ├── dynamic_tables.py # 动态表格数据操作
    └── debug.py         # 调试接口
```

## 默认账户

初始化数据后会创建一个默认管理员账户:

- 用户名: admin
- 密码: admin123
