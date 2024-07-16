# 开发环境配置

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ninja_demo",  # 你的数据库名
        "USER": "root",  # 你的数据库用户名
        "PASSWORD": "123456",  # 你的数据库密码
        "HOST": "127.0.0.1",  # 数据库服务器地址，如果是本地则为localhost
        "PORT": "3307",  # MySQL默认端口
        "POOL_OPTIONS": {
            "POOL_SIZE": 10,
            "MAX_OVERFLOW": 10,
            "TIMEOUT": 3600,
        },
    }
}

# 打印sql语句
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
