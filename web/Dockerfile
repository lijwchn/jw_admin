# 第一阶段：使用 Node.js 镜像进行构建
FROM node:18.20.4-alpine3.20 AS builder

# 设置工作目录
WORKDIR /app

# 复制依赖文件，以便利用缓存
COPY package.json yarn.lock ./

# 安装依赖
RUN yarn install

# 复制前端项目文件并进行构建
COPY . /app
RUN yarn build

# 第二阶段：使用 Nginx 镜像进行部署
FROM nginx:alpine

# 复制 Nginx 配置文件到容器内
COPY nginx.conf /etc/nginx/nginx.conf
# 复制构建阶段生成的静态文件到 Nginx 的默认静态文件目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露 Nginx 服务器端口
EXPOSE 80

# 启动 Nginx 服务器
CMD ["nginx", "-g", "daemon off;"]