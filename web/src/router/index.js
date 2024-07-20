import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Welcome from '@/views/Welcome.vue'
import Login from '@/views/Login.vue'

const routes = [
  {
    name: 'home',
    path: '/',
    meta: {
      title: '首页',
    },
    component: Home,
    redirect: '/welcome',
    children: [
      {
        name: 'welcome',
        // 注意，这里的path不要带 /,因为上面的父路由已经有/
        path: 'welcome',
        meta: {
          title: '欢迎页',
        },
        component: Welcome,
      },
      {
        name: 'user',
        path: '/system/user',
        meta: {
          title: '用户管理',
        },
        component: () => import('@/views/User.vue'),
      },
      {
        name: 'menu',
        path: '/system/menu',
        meta: {
          title: '菜单管理',
        },
        component: () => import('@/views/Menu.vue'),
      },
      {
        name: 'role',
        path: '/system/role',
        meta: {
          title: '角色管理',
        },
        component: () => import('@/views/Role.vue'),
      },
      {
        name: 'dept',
        path: '/system/dept',
        meta: {
          title: '部门管理',
        },
        component: () => import('@/views/Dept.vue'),
      },
      {
        name: 'barcode',
        path: '/tools/barcode',
        meta: {
          title: '条形码',
        },
        component: () => import('@/views/BarCode.vue'),
      },
      {
        name: 'create_barcode',
        path: '/tools/create_barcode',
        meta: {
          title: '生成条形码',
        },
        component: () => import('@/views/GenBarCode.vue'),
      },
      {
        name: 'pic_ocr',
        path: '/tools/pic_ocr',
        meta: {
          title: 'ocr图片识别',
        },
        component: () => import('@/views/OcrTool.vue'),
      },
      {
        name: 'demo1',
        path: '/learn/demo1',
        meta: {
          title: '学习菜单1',
        },
        component: () => import('@/demo/demo1.vue'),
      },
      {
        name: 'demo2',
        path: '/learn/demo2',
        meta: {
          title: '学习菜单2',
        },
        component: () => import('@/demo/demo2.vue'),
      },
    ],
  },
  {
    name: 'login',
    path: '/login',
    meta: {
      title: '登录页',
    },
    component: Login,
  },
  {
    name: '404',
    path: '/404',
    meta: {
      title: '404页面',
    },
    component: () => import('@/views/404.vue'),
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

// 判断当前传过来的path是否在router对象中有对应的数据
// 使用filter在数组中过滤
const checkPermission = (path) => {
  let hasPermission = router
    .getRoutes()
    .filter((route) => route.path == path).length
  if (hasPermission) {
    return true
  } else {
    return false
  }
}

router.beforeEach((to, from, next) => {
  if (checkPermission(to.path)) {
    document.title = to.meta.title
    next()
  } else {
    next('/404')
  }
})

export default router
