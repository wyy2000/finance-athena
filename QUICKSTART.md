# 快速开始指南

## 🚀 快速启动

### 方式一：Docker一键启动（推荐）

```bash
# 1. 启动所有服务
./start.sh

# 2. 访问系统
# 前端页面: http://localhost:8000
# API文档: http://localhost:8000/docs

# 3. 测试API
python test_api.py
```

### 方式二：本地开发环境

```bash
# 1. 设置Python虚拟环境
cd backend
./setup_venv.sh

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 配置环境变量
cp env.example .env

# 4. 启动MySQL和Redis（需要本地安装）
# 或者使用Docker启动数据库
docker-compose up -d db redis

# 5. 启动开发服务器
./dev.sh
```

## 🔑 初始账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| junior1 | password123 | 初级审核员 |
| senior1 | password123 | 中级审核员 |
| expert1 | password123 | 高级审核员 |
| committee1 | password123 | 投资委员会 |

## 📋 功能测试

### 1. 客户注册测试
```bash
curl -X POST "http://localhost:8000/api/v1/customers/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "phone": "13800138000",
    "id_card": "110101199001011234",
    "email": "zhangsan@example.com",
    "occupation": "工程师",
    "investment_amount": 500000,
    "assessment_data": {
      "age": "31-45岁",
      "income": "30-50万",
      "experience": "3-5年",
      "risk_tolerance": "15-30%",
      "goal": "积极增长",
      "period": "3-5年"
    }
  }'
```

### 2. 审核员登录测试
```bash
curl -X POST "http://localhost:8000/api/v1/auditors/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "junior1",
    "password": "password123"
  }'
```

### 3. 获取工作台数据
```bash
# 先获取token（从登录响应中获取）
curl -X GET "http://localhost:8000/api/v1/workflow/workflow" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🛠️ 开发工具

### 虚拟环境管理
```bash
# 创建虚拟环境
./setup_venv.sh

# 激活虚拟环境
source venv/bin/activate

# 退出虚拟环境
deactivate
```

### 开发服务器
```bash
# 启动开发服务器（自动重载）
./dev.sh

# 或手动启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 测试
```bash
# 运行API测试
./test_local.sh

# 或手动运行
python test_api.py
```

### 数据库管理
```bash
# 查看数据库日志
docker-compose logs db

# 进入数据库
docker-compose exec db mysql -u root -p finance_athena

# 重置数据库
docker-compose down -v
docker-compose up -d
```

## 📁 项目结构说明

```
backend/
├── app/                    # 应用代码
│   ├── api/               # API路由
│   ├── models/            # 数据模型
│   ├── schemas/           # 数据验证
│   ├── services/          # 业务逻辑
│   └── utils/             # 工具函数
├── venv/                  # Python虚拟环境
├── requirements.txt       # Python依赖
├── setup_venv.sh         # 虚拟环境设置
├── dev.sh                # 开发服务器启动
└── test_local.sh         # 本地测试
```

## 🔧 常见问题

### 1. 端口被占用
```bash
# 查看端口占用
lsof -i :8000

# 杀死进程
kill -9 PID
```

### 2. 数据库连接失败
```bash
# 检查数据库状态
docker-compose ps

# 重启数据库
docker-compose restart db
```

### 3. 虚拟环境问题
```bash
# 重新创建虚拟环境
rm -rf venv
./setup_venv.sh
```

### 4. 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

## 📞 技术支持

如果遇到问题，请检查：
1. Python版本是否为3.10
2. Docker和Docker Compose是否安装
3. 端口8000、3306、6379是否被占用
4. 网络连接是否正常
