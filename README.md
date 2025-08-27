# 银行投资风险审核系统

## 项目简介

银行投资风险审核系统是一个基于Python 3.10和MySQL的智能化投资风险评估和审核平台。系统能够根据客户的基本信息、财务状况和风险偏好，自动化地进行风险评估和投资建议生成，并通过多级审核机制确保审核流程的规范性和准确性。

## 技术栈

- **后端**: Python 3.10 + FastAPI
- **数据库**: MySQL 8.0
- **前端**: HTML + CSS + JavaScript
- **缓存**: Redis
- **部署**: Docker + Docker Compose

## 功能特性

### 客户功能
- 客户信息注册
- 风险评估问卷
- 智能风险评分
- 投资建议生成
- 审核状态查询

### 审核员功能
- 多级审核流程
- 审核工作台
- 客户信息管理
- 投资建议审核
- 审核结果通知

## 快速开始

### 环境要求
- Docker
- Docker Compose

### 启动步骤

1. 克隆项目
```bash
git clone <repository-url>
cd finance-athena
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问系统
- 前端页面: http://localhost:8000
- API文档: http://localhost:8000/docs

### 初始账号

系统预置了以下审核员账号：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| junior1 | password123 | 初级审核员 |
| senior1 | password123 | 中级审核员 |
| expert1 | password123 | 高级审核员 |
| committee1 | password123 | 投资委员会 |

## API接口

### 客户相关接口
- `POST /api/v1/customers/register` - 客户注册和风险评估
- `GET /api/v1/customers/{customer_id}` - 获取客户信息
- `GET /api/v1/customers/{customer_id}/advice` - 获取投资建议

### 审核员相关接口
- `POST /api/v1/auditors/login` - 审核员登录
- `GET /api/v1/auditors/me` - 获取当前审核员信息

### 工作流相关接口
- `GET /api/v1/workflow/workflow` - 获取审核工作台数据
- `POST /api/v1/workflow/audit` - 提交审核结果

## 项目结构

```
finance-athena/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── requirements.txt    # Python依赖
│   ├── setup_venv.sh      # 虚拟环境设置脚本
│   ├── dev.sh             # 开发环境启动脚本
│   ├── test_local.sh      # 本地测试脚本
│   ├── env.example        # 环境变量示例
│   └── Dockerfile         # Docker配置
├── frontend/               # 前端代码
│   ├── index.html         # 主页面
│   └── demo/              # 演示页面
├── database/              # 数据库脚本
│   └── init.sql          # 初始化脚本
├── docker-compose.yml     # Docker Compose配置
├── start.sh              # 一键启动脚本
├── test_api.py           # API测试脚本
├── .gitignore            # Git忽略文件
└── README.md             # 项目说明
```

## 开发说明

### 本地开发

#### 方法一：使用虚拟环境（推荐）

1. 设置Python虚拟环境
```bash
cd backend
./setup_venv.sh
```

2. 激活虚拟环境
```bash
source venv/bin/activate
```

3. 配置环境变量
```bash
cp env.example .env
# 根据需要修改.env文件中的配置
```

4. 启动开发服务器
```bash
./dev.sh
```

#### 方法二：直接安装依赖

1. 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

2. 配置数据库
```bash
# 创建MySQL数据库
mysql -u root -p < database/init.sql
```

3. 启动后端服务
```bash
cd backend
uvicorn app.main:app --reload
```

### 环境变量配置

复制环境变量示例文件：
```bash
cd backend
cp env.example .env
```

根据需要修改 `.env` 文件中的配置：
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/finance_athena
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=银行投资风险审核系统
DEBUG=true
```

## 审核流程

### 保守型投资者
1. 客户提交信息 → 2. 系统风险评估 → 3. 初级审核员审核 → 4. 审核完成

### 稳健型投资者
1. 客户提交信息 → 2. 系统风险评估 → 3. 初级审核员审核 → 4. 中级审核员审核 → 5. 审核完成

### 激进型投资者
1. 客户提交信息 → 2. 系统风险评估 → 3. 初级审核员审核 → 4. 中级审核员审核 → 5. 高级审核员审核 → 6. 投资委员会审核 → 7. 审核完成

## 许可证

MIT License
