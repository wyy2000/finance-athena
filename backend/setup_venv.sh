#!/bin/bash

echo "🐍 设置Python虚拟环境..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -o '3\.[0-9]\+')
if [[ $python_version != 3.10* ]]; then
    echo "❌ 需要Python 3.10，当前版本: $python_version"
    echo "请安装Python 3.10或使用pyenv管理Python版本"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 检查是否已存在虚拟环境
if [ -d "venv" ]; then
    echo "📁 虚拟环境已存在，是否重新创建？(y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "🗑️ 删除现有虚拟环境..."
        rm -rf venv
    else
        echo "✅ 使用现有虚拟环境"
        exit 0
    fi
fi

# 创建虚拟环境
echo "🔨 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "⬆️ 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

echo ""
echo "✅ 虚拟环境设置完成！"
echo ""
echo "🔧 激活虚拟环境："
echo "   source venv/bin/activate"
echo ""
echo "🚀 启动开发服务器："
echo "   uvicorn app.main:app --reload"
echo ""
echo "🔍 运行测试："
echo "   python test_api.py"
