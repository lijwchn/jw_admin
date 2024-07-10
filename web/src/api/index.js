import request from '@/utils/request'

export default {
  login(params) {
    return request({
      url: '/auth/login',
      data: params,
      method: 'post',
    })
  },
  // 获取通知
  getNoticeCount() {
    return request({
      url: '/mock/leave/count',
      method: 'get',
    })
  },
  // 获取用户菜单和按钮权限列表
  getUserMenuList() {
    return request({
      url: '/system/user_permissions',
      method: 'get',
    })
  },
  // 查所有用户
  getUserList(params) {
    return request({
      url: '/system/user',
      method: 'get',
      data: params,
    })
  },
  // 删除用户
  deleteUser(params) {
    return request({
      url: '/system/batch_delete_user',
      method: 'post',
      data: params,
    })
  },
  // 创建用户
  createUser(params) {
    return request({
      url: '/system/user',
      method: 'post',
      data: params,
    })
  },

  // 根据id获取用户详情
  getUserDetailById(id) {
    return request({
      url: `/system/user/${id}`,
      method: 'get',
    })
  },
  // 编辑用户
  updateUserInfo(params) {
    return request({
      url: `/system/user`,
      method: 'put',
      data: params,
    })
  },
  // 查询全部菜单列表
  getAllMenuList(params) {
    return request({
      url: `/system/menu_list`,
      method: 'post',
      data: params,
    })
  },
  // 创建菜单
  createMenu(params) {
    return request({
      url: `/system/menu`,
      method: 'post',
      data: params,
    })
  },
  // 获取单个菜单的详情
  getMenuDetialById(menu_id) {
    return request({
      url: `/system/menu/${menu_id}`,
      method: 'get',
    })
  },
  // 更新菜单
  updateMenu(params) {
    return request({
      url: `/system/menu`,
      method: 'put',
      data: params,
    })
  },
  // 删除菜单
  deleteMenu(menu_id) {
    return request({
      url: `/system/menu/${menu_id}`,
      method: 'delete',
    })
  },
  // 获取角色列表
  getRoleList(params) {
    return request({
      url: '/system/role',
      method: 'get',
      data: params,
    })
  },
  // 创建角色
  createRole(params) {
    return request({
      url: `/system/role`,
      method: 'post',
      data: params,
    })
  },
  // 根据id获取单个角色详情
  getRoleDetail(role_id) {
    return request({
      url: `/system/role/${role_id}`,
      method: 'get',
    })
  },
  // 更新角色
  updateRole(params) {
    return request({
      url: `/system/role`,
      method: 'put',
      data: params,
    })
  },
  // 给角色分配权限
  assiginPerToRole(role_id, params) {
    return request({
      url: `/system/role/${role_id}/menu`,
      method: 'post',
      data: params,
    })
  },
  // 删除角色
  deleteRole(role_id) {
    return request({
      url: `/system/role/${role_id}`,
      method: 'delete',
    })
  },
  // 获取部门列表
  getDeptList(params) {
    return request({
      url: '/system/dept',
      method: 'get',
      data: params,
    })
  },
  // 查询单个部门详情
  getDeptDetial(dept_id) {
    return request({
      url: `/system/dept/${dept_id}`,
      method: 'get',
    })
  },
  // 新增部门
  createDept(params) {
    return request({
      url: `/system/dept`,
      method: 'post',
      data: params,
    })
  },
  // 修改部门
  updateDept(dept_id, params) {
    return request({
      url: `/system/dept/${dept_id}`,
      method: 'put',
      data: params,
    })
  },
  // 删除部门
  deleteDept(dept_id) {
    return request({
      url: `/system/dept/${dept_id}`,
      method: 'delete',
    })
  },
  // 获取用户当前角色所有的菜单
  getUserMenuPermission() {
    return request({
      url: `/system/user_permissions`,
      method: 'get',
    })
  },
  // 修改密码
  changePassword(params) {
    return request({
      url: `/system/update_password`,
      method: 'post',
      data: params,
    })
  },
  // mock接口，下单
  createOrder() {
    return request({
      url: `/mock/create_order/9`,
      method: 'get',
    })
  },
}
