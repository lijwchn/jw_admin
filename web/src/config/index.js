/**
 * 环境配置封装
 */
const env = import.meta.env.MODE || 'prod'
console.log('当前环境', env)
const EnvConfig = {
  development: {
    baseApi: 'http://127.0.0.1:8000/v1',
    mockApi: 'http://127.0.0.1:8001/api',
  },
  test: {
    baseApi: '/',
    mockApi: 'http://127.0.0.1:8001/api',
  },
  prod: {
    baseApi: '/',
    mockApi: 'http://127.0.0.1:8002/api',
  },
}

export default {
  env,
  mock: true,
  ...EnvConfig[env],
  namespace: 'manage',
}
