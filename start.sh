#!/bin/bash

echo "🚀 启动银行投资风险审核系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

echo ""
echo "✅ 系统启动完成！"
echo ""
echo "🌐 访问地址："
echo "   前端页面: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "🔑 初始审核员账号："
echo "   用户名: junior1, senior1, expert1, committee1"
echo "   密码: password123"
echo ""
echo "📝 查看日志：docker-compose logs -f"
echo "🛑 停止服务：docker-compose down"
