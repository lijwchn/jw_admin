# 一个简易的 rbac 权限管理系统

### 在线体验环境

浏览器访问：[点我](http://106.52.59.119/)

## 开发环境运行调试

### 1. 后端 django + django ninja + mysql

python 版本 3.11
1. 修改配置文件，在 ninja_demo.settings 文件夹下的 dev.py 中修改配置
2. 需要保证 mysql 数据库已经创建好
3. 迁移数据库，切换到项目根目录下，执行 python manage.py migrate
4. 创建管理员用户，执行 python manage.py createsuperuser，创建成功后，在 system_users 表中能找到
5. 在 ninja_demo/init.sql 中，执行 sql 脚本，创建菜单、角色和权限

### 2. 前端 vue3+vite+element-plus

node 版本 18

1. 切换到 web/src/config/index.js ，修改开发环境的后端地址
2. 切换到 web 目录下，执行 yarn，然后 yarn dev 启动项目

## 生产环境部署（docker环境）：

1. 后端：修改配置文件，在 ninja_demo.settings 文件夹下的 prod.py 中修改配置
2. 前端：切换到 web/src/config/index.js ，修改生产环境的后端地址
3. 前端：切换到 web 目录下，按照你的实际情况，修改 nginx.conf 文件
4. 开始部署，docker-compose up --build

## 说明

这个项目原来是放在gitee的，现在整合在一起之后可以一次性使用 docker 部署

原先项目地址:

前端：https://gitee.com/lijwchn/vue3_manage_learn

后端：https://gitee.com/lijwchn/ninja_demo
