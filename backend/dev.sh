#!/bin/bash

echo "🚀 启动开发环境..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 setup_venv.sh"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查依赖是否安装
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 安装依赖..."
    pip install -r requirements.txt
fi

# 启动开发服务器
echo "🌐 启动开发服务器..."
echo "   访问地址: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo "   按 Ctrl+C 停止服务器"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
