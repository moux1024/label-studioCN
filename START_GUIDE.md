# Label Studio 启动指南

本项目有多种启动方式，根据你的需求选择合适的方式。

## 🚀 快速启动（推荐）

### 方式一：使用 Docker Compose（最简单）

这是最简单的方式，适合快速体验和开发：

```bash
# 1. 启动所有服务（包括后端、前端、数据库）
docker-compose up

# 或者后台运行
docker-compose up -d

# 2. 访问应用
# 打开浏览器访问: http://localhost:8080
```

**停止服务：**
```bash
docker-compose down
```

### 方式二：本地开发模式（需要安装依赖）

适合需要修改代码的开发场景：

#### 前置要求
- Python >= 3.8
- Node.js 和 Yarn
- Poetry（Python 包管理工具）

#### 步骤 1：安装后端依赖

```bash
# 安装 poetry（如果还没有）
pip install poetry

# 安装 Python 依赖
poetry install

# 运行数据库迁移
make migrate-dev
# 或者
DJANGO_DB=sqlite LOG_DIR=tmp DEBUG=true LOG_LEVEL=DEBUG DJANGO_SETTINGS_MODULE=core.settings.label_studio poetry run python label_studio/manage.py migrate

# 收集静态文件
poetry run python label_studio/manage.py collectstatic
```

#### 步骤 2：安装前端依赖

```bash
# 进入 web 目录
cd web

# 安装前端依赖
yarn install --frozen-lockfile

# 或者使用 Makefile（在项目根目录）
make frontend-install
```

#### 步骤 3：启动服务

**选项 A：使用 Makefile（推荐）**

```bash
# 在项目根目录

# 启动后端开发服务器（终端1）
make run-dev

# 启动前端开发服务器（终端2）
make frontend-dev
```

**选项 B：手动启动**

```bash
# 终端1：启动后端
DJANGO_DB=sqlite LOG_DIR=tmp DEBUG=true LOG_LEVEL=DEBUG DJANGO_SETTINGS_MODULE=core.settings.label_studio poetry run python label_studio/manage.py runserver

# 终端2：启动前端（在 web 目录下）
cd web
yarn dev
```

**访问地址：**
- 后端 API: http://localhost:8080
- 前端应用: http://localhost:8080（如果启用了 HMR，前端会在 http://localhost:8010）

## 📋 其他启动方式

### 使用 pip 安装（生产环境）

```bash
# 安装
pip install label-studio

# 启动
label-studio
# 访问 http://localhost:8080
```

### 使用 Docker 镜像

```bash
# 拉取镜像
docker pull heartexlabs/label-studio:latest

# 运行容器
docker run -it -p 8080:8080 -v $(pwd)/mydata:/label-studio/data heartexlabs/label-studio:latest

# 访问 http://localhost:8080
```

## 🔧 开发模式配置

### 启用热模块替换（HMR）

如果你想在开发时启用前端热更新：

1. 在项目根目录创建 `.env` 文件：
```bash
FRONTEND_HMR=true
FRONTEND_HOSTNAME=http://localhost:8010
DJANGO_HOSTNAME=http://localhost:8080
```

2. 如果使用 Docker，还需要配置 `docker-compose.override.yml`：
```bash
make docker-dev-setup
```

3. 启动开发服务器：
```bash
# 从项目根目录
make frontend-dev

# 或从 web 目录
cd web && yarn dev
```

## 📝 常用命令

### 后端命令（使用 Makefile）

```bash
# 启动开发服务器
make run-dev

# 运行数据库迁移
make migrate-dev

# 创建数据库迁移
make makemigrations-dev

# Django shell
make shell-dev
```

### 前端命令（在 web 目录下）

```bash
# 开发模式（带 HMR）
yarn dev

# 监听模式（自动构建）
yarn watch

# 构建生产版本
yarn build

# 运行 Storybook（UI 组件库）
yarn ui:serve

# 运行测试
yarn test:unit
```

### 前端命令（使用 Makefile，在项目根目录）

```bash
# 安装前端依赖
make frontend-install

# 启动前端开发服务器
make frontend-dev

# 监听模式
make frontend-watch

# 构建生产版本
make frontend-build

# 启动 Storybook
make frontend-storybook-serve
```

## 🐳 Docker 相关命令

```bash
# 启动开发环境（带 HMR）
make docker-dev-setup
make docker-run-dev

# 运行数据库迁移
make docker-migrate-dev

# 收集静态文件
make docker-collectstatic-dev

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f
```

## ⚠️ 常见问题

### 1. 端口被占用

如果 8080 端口被占用，可以修改端口：

**Docker 方式：**
修改 `docker-compose.yml` 中的端口映射

**本地方式：**
```bash
# 后端
python label_studio/manage.py runserver 8081

# 前端（修改 web/package.json 或环境变量）
```

### 2. 数据库连接错误

确保：
- SQLite：数据库文件有写入权限
- PostgreSQL：数据库服务已启动，配置正确

### 3. 前端依赖安装失败

```bash
# 清除缓存重试
cd web
rm -rf node_modules yarn.lock
yarn install --frozen-lockfile
```

### 4. Python 依赖问题

```bash
# 使用 poetry 重新安装
poetry install --no-cache
```

## 📚 更多信息

- 详细文档：查看 `README.md` 和 `web/README.md`
- API 文档：启动后访问 http://localhost:8080/api/docs
- 前端组件：运行 `yarn ui:serve` 查看 Storybook

## 🎯 推荐开发流程

1. **首次启动：**
   ```bash
   # 使用 Docker（最简单）
   docker-compose up
   ```

2. **本地开发：**
   ```bash
   # 终端1：后端
   make run-dev
   
   # 终端2：前端
   make frontend-dev
   ```

3. **查看效果：**
   - 打开浏览器访问 http://localhost:8080
   - 查看中文界面效果（已替换的文本）

