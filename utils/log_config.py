from loguru import logger
import sys

# 移除默认的日志配置,可以避免默认的日志输出，同时避免重复日志输出的问题
logger.remove()
# 添加一个新的日志处理器，将日志输出到控制台。sys.stdout 表示标准输出
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
# 添加一个新的日志处理器，将日志输出到文件 logs/app.log
# level="DEBUG" 设置日志级别为 DEBUG，表示输出 DEBUG 及更高级别的日志
logger.add("logs/app.log", rotation="500 MB", retention="10 days", level="DEBUG")
