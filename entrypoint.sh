#!/bin/sh

# 等待数据库服务启动并准备好连接
while ! nc -z db 3306; do
  echo "等待数据库服务启动..."
  sleep 1
done

# 迁移数据库
python manage.py migrate

# 启动 Django 应用
exec "$@"
