# 基于大语言模型的后台管理生成系统

基于 Flask + Vue和大语言模型的后台管理生成系统，允许通过输入管理需求，再经过大语言的润色修改后，大语言模型进行思考并生成代码，最后可以将代码复制或者下载下来。

## 项目特点

- 前后端分离架构
- 支持生成任意管理系统
- 流式输出大语言模型的输出内容
- 支持多种字段类型
- 可以将代码按文件分类后下载下来或者按单个文件复制下来

## 技术栈

### 前端
- Vue.js 3.x
- Vue Router 4.x
- Element Plus (UI组件库)
- Axios (HTTP客户端)

### 后端
- Python 3.x
- Flask 框架
- SQLAlchemy ORM
- 支持 MySQL 数据库

## 项目结构

```
/
├── README.md                     # 项目说明书
├── .venv/                        # 后端虚拟环境
├── static/
    ├── index.html                # 接口测试的HTML模板
├── backend/                      # 后端 Flask 应用                  
|   ├── .env.example              # 环境示例
│   ├── app.py                    # 应用入口
│   ├── dify_generation.py        # Dify API交互工具
|   └── langchain_generation.py   # 基于DeepSeek的模块设计与表结构生成器
└── frontend/                     # 前端 Vue 应用
    ├── src/                      # 源代码
    │   ├── assets/               # 资源文件
    │   ├── components/           # 组件
    │   ├── layouts/              # 布局组件
    │   ├── router/               # 路由
    │   ├── stores/               # 状态管理
    │   ├── views/                # 页面视图
    |   ├── utils                 # 工具
    │   ├── App.vue               # 根组件
    │   └── main.js               # 入口文件
    └── tests/                    # 初期测试文件
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
   # 编辑 .env 文件，设置API_KEY
   ```

4. 运行后端服务
   ```bash
   python app.py  # 默认在 8000 端口
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

1. 输入需要生成的管理系统的需求
   - 自己输入详细内容
   - 输入简略内容后由大语言润色为详细内容

2. 生成代码
    - 大语言模型根据输入框的内容进行思考后生成代码

3. 代码展示
   - 代码生成完毕后将代码显示出来
   - 可以选择将代码下载到本地
   - 可以将单个的代码文件进行复制

## 字段类型支持

- 文本 (text) - 短文本
- 长文本 (longtext) - 多行文本
- 数字 (number) - 浮点数
- 整数 (integer) - 整数
- 日期 (date) - 日期选择器
- 日期时间 (datetime) - 日期和时间选择器
- 布尔值 (boolean) - 开关 
