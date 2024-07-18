# 后端 python Dockerfile
FROM python:3.11-alpine

# 设置工作目录
WORKDIR /app

# 添加必要的软件包(更换成阿里云镜像源)
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk add --no-cache pkgconfig mysql-dev build-base

# 先复制依赖文件，以便利用缓存
COPY requirements.txt /app/
RUN pip install --no-cache-dir -i https://mirrors.cloud.tencent.com/pypi/simple -r requirements.txt

# 再复制项目文件
COPY . /app
# 设置 Django 的配置文件使用生产环境
ENV DJANGO_SETTINGS_MODULE=ninja_demo.settings.prod

# 暴露端口
EXPOSE 8000
# 设置权限
RUN chmod +x /app/entrypoint.sh
# 设置 entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# 启动 Django 应用
CMD ["gunicorn", "ninja_demo.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "5"]
