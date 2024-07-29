# 生产环境配置
from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = [
    "localhost",  # 如果你的开发环境也是通过localhost访问
    "127.0.0.1",  # 如果你的开发环境也是通过127.0.0.1访问
    "106.52.59.119",  # 添加你的服务器IP地址
]

# 允许所有来源都能访问，为了解决 cors 跨域问题
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),  # 你的数据库名
        "USER": os.getenv("DB_USER", "root"),  # 你的数据库用户名
        "PASSWORD": os.getenv("DB_PASSWORD"),  # 你的数据库密码
        "HOST": os.getenv("DB_HOST"),  # 数据库服务器地址，如果是本地则为localhost
        "PORT": os.getenv("DB_PORT"),  # MySQL默认端口
        "POOL_OPTIONS": {
            "POOL_SIZE": 10,
            "MAX_OVERFLOW": 10,
            "TIMEOUT": 3600,
        },
    }
}
