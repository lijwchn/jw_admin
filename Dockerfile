# 后端 python Dockerfile
FROM python:3.11-alpine

# 设置工作目录
WORKDIR /app

# 添加必要的软件包
RUN apk add --no-cache pkgconfig mariadb-dev mysql-dev build-base

# 克隆最新代码
COPY . /app


# 安装依赖
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 迁移数据库文件
#RUN python manage.py migrate
# 设置 Django 环境变量
ENV DJANGO_SETTINGS_MODULE=ninja_demo.settings.prod

# 暴露端口
EXPOSE 8000

# 设置 entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# 启动 Django 应用
CMD ["gunicorn", "ninja_demo.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "5"]
