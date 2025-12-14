#!/bin/bash
# 修复 react-app 目录结构的脚本
# 将构建的文件复制到 react-app 子目录中，以便 Django 能够正确访问

cd "$(dirname "$0")/.." || exit 1

REACT_APP_DIR="web/dist/apps/labelstudio/react-app"

echo "修复 react-app 目录结构..."

# 创建 react-app 目录
mkdir -p "$REACT_APP_DIR"

# 复制必要的文件到 react-app 目录
if [ -f "web/dist/apps/labelstudio/main.js" ]; then
    cp web/dist/apps/labelstudio/main.js "$REACT_APP_DIR/"
    cp web/dist/apps/labelstudio/main.css "$REACT_APP_DIR/" 2>/dev/null || true
    cp web/dist/apps/labelstudio/runtime.js "$REACT_APP_DIR/" 2>/dev/null || true
    cp web/dist/apps/labelstudio/vendor.js "$REACT_APP_DIR/" 2>/dev/null || true
    echo "✅ 已复制文件到 react-app 目录"
else
    echo "❌ 错误: 找不到构建文件，请先运行 'yarn build' 或 'make frontend-build'"
    exit 1
fi

echo "完成！现在 Django 应该能够访问 /react-app/main.js 了"

