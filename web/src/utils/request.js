/**
 * axios二次封装
 */
import axios from 'axios'
import config from './../config'
import { ElMessage } from 'element-plus'
import router from './../router'
import storage from '@/utils/storage'

const TOKEN_INVALID = 'Token认证失败，请重新登录'
const NETWORK_ERROR = '网络请求异常，请稍候重试'

// 创建 axios 实例对象，添加全局配置
const service = axios.create({
  baseURL: config.baseApi,
  timeout: 8000,
})

// 请求拦截
service.interceptors.request.use((req) => {
  const headers = req.headers
  if (!headers.Authorization)
    headers.Authorization = storage.getItem('userToken')
  // console.log('用户信息', storage.getItem('userInfo'))
  return req
})

// 响应拦截
service.interceptors.response.use(
  (res) => {
    console.log('res', res)
    // 解构后端api返回的数据
    const { code, data, message, success } = res.data
    if (code === 200 && success) {
      // 将后端原始的响应报文返回
      return res.data
    } else {
      ElMessage.error(message || NETWORK_ERROR)
      return Promise.reject(message || NETWORK_ERROR)
    }
  },
  // 所有状态码非 2xx 的请求都会走到下面的逻辑
  (error) => {
    if (!error.response) {
      ElMessage.error(NETWORK_ERROR)
      return Promise.reject(new Error(NETWORK_ERROR))
    }
    if (error.response.status === 401) {
      ElMessage.error(TOKEN_INVALID)
      setTimeout(() => {
        router.push('/login')
      }, 1500)
      return Promise.reject(new Error(TOKEN_INVALID))
    }
    if (error.response.status === 404) {
      ElMessage.error('接口404，资源不存在')
    }
    ElMessage.error(NETWORK_ERROR)
    return Promise.reject(error)
  }
)

/**
 *
 * @param {*} options
 * @returns
 */
function request(options) {
  options.method = options.method || 'get'
  if (options.method.toLowerCase() === 'get') {
    options.params = options.data
  }
  // 优先取 api 实例中的mock的值，而不是全局mock的值
  if (typeof options.mock != 'undefined') {
    config.mock = options.mock
  }

  if (config.env === 'prod') {
    service.defaults.baseURL = config.baseApi
  } else {
    service.defaults.baseURL = config.mock ? config.mockApi : config.baseApi
  }
  return service(options)
}

const reqMethod = ['get', 'post', 'put', 'delete', 'patch']

reqMethod.forEach((item) => {
  request[item] = (url, data, options) => {
    return request({
      url,
      data,
      method: item,
      ...options,
    })
  }
})

export default request
