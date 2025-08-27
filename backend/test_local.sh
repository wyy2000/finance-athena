#!/bin/bash

echo "🧪 运行本地测试..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 setup_venv.sh"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查依赖是否安装
if ! python -c "import requests" 2>/dev/null; then
    echo "📦 安装测试依赖..."
    pip install requests
fi

# 运行测试
echo "🔍 运行API测试..."
python test_api.py
