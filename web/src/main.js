import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn' // el-p 中文
import 'element-plus/dist/index.css'
import request from './utils/request'
import api from '@/api/index'
import storage from './utils/storage'
import store from './store'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const app = createApp(App)
// 引入 element 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(router) // 挂载路由
app.use(ElementPlus, { locale: zhCn }) // 挂载ui组件，并且使用中文
app.use(store)
app.config.globalProperties.$request = request // 全局挂载发送网络请求
app.config.globalProperties.$api = api // 全局挂载发送网络请求
app.config.globalProperties.$storage = storage // 全局挂载本地存储
app.config.globalProperties.$message = ElMessage // 全局挂载el-message
app.mount('#app')
