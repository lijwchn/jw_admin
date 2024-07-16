# 第一阶段：使用 Node.js 镜像进行构建
FROM node:17 AS builder

# 设置工作目录
WORKDIR /app

# 克隆最新代码
#RUN git clone https://github.com/lijwchn/jw_admin.git .

# 复制 package.json 和 yarn.lock 文件并安装依赖
COPY package.json yarn.lock ./
RUN yarn install

# 复制所有项目文件到工作目录并进行构建
COPY . .
RUN yarn build

# 第二阶段：使用 Nginx 镜像进行部署
FROM nginx:alpine

# 复制构建阶段生成的静态文件到 Nginx 的默认静态文件目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露 Nginx 服务器端口
EXPOSE 80

# 启动 Nginx 服务器
CMD ["nginx", "-g", "daemon off;"]