/**
 * 环境配置封装
 */
const env = import.meta.env.MODE || 'production'
console.log('当前环境', env)
const EnvConfig = {
  development: {
    baseApi: 'http://127.0.0.1:8001/api',
    mockApi: 'http://127.0.0.1:8001/api',
  },
  test: {
    baseApi: '/',
    mockApi: 'http://127.0.0.1:8001/api',
  },
  production: {
    baseApi: 'http:///backend/api',
    mockApi: 'http://127.0.0.1:8002/mock', // 实际上没有mock这个地址
  },
}

export default {
  env,
  mock: true,
  ...EnvConfig[env],
  namespace: 'manage',
}
