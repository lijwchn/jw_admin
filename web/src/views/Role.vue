<template>
  <div class="role-manage">
    <div class="query-form">
      <el-form :inline="true" :model="roleQueryForm" ref="roleQueryFormRef">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleQueryForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色状态" prop="status">
          <el-select
            v-model="roleQueryForm.status"
            style="width: 100px"
            placeholder="选择状态"
            clearable
          >
            <el-option :value="true" label="启用"></el-option>
            <el-option :value="false" label="停用"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleResetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="base-table">
      <!-- 操作按钮区域 -->
      <div class="action">
        <el-button type="primary" @click="handleCreateRole">新增</el-button>
      </div>
      <div class="table-content">
        <el-table :data="roleList" border>
          <el-table-column
            v-for="item in columns"
            :key="item.id"
            :prop="item.prop"
            :label="item.label"
            :formatter="item.formatter"
          >
          </el-table-column>

          <el-table-column label="操作" min-width="100">
            <!-- #default="rowContent" 表示当前行的数据 -->
            <template #default="rowContent">
              <el-button size="small" @click="handleEdit(rowContent.row)"
                >编辑</el-button
              >
              <el-button
                size="small"
                type="primary"
                @click="handlePermission(rowContent.row)"
                >权限管理</el-button
              >
              <el-popconfirm
                confirm-button-text="是"
                confirm-button-type="danger"
                cancel-button-text="否"
                cancel-button-type="primary"
                icon-color="#f56c6c"
                title="确认删除？"
                @confirm="handleDel(rowContent.row)"
              >
                <template #reference>
                  <el-button size="small" type="danger">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination
        class="pagination-container"
        :page-sizes="[10, 30, 50]"
        layout="sizes, prev, pager, next, total"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
      <el-dialog
        :title="isEditMode ? '编辑角色' : '新增角色'"
        v-model="showRoleForm"
        :before-close="handleClose"
      >
        <el-form
          :model="roleForm"
          label-width="100px"
          ref="roleFormRef"
          :rules="rules"
        >
          <el-form-item label="角色名称" prop="name">
            <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
          </el-form-item>
          <el-form-item label="角色编码" prop="code">
            <el-input
              v-model="roleForm.code"
              placeholder="请输入角色编码（需要唯一）"
            />
          </el-form-item>
          <el-form-item label="角色状态" prop="status">
            <el-radio-group v-model="roleForm.status">
              <el-radio-button label="启用" :value="true"></el-radio-button>
              <el-radio-button label="停用" :value="false"></el-radio-button>
            </el-radio-group>
            <div style="padding-left: 40px">如果不选，默认为启用状态</div>
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input
              type="textarea"
              v-model="roleForm.remark"
              placeholder="请输入备注"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="handleClose">取消</el-button>
            <el-button type="primary" @click="handleSubmit">确定</el-button>
          </div>
        </template>
      </el-dialog>
      <el-dialog title="角色权限管理" v-model="showRolePermission">
        <el-tree
          :data="menuList"
          :props="permissionTreeProps"
          show-checkbox
          node-key="id"
          default-expand-all
          clearable
          ref="permissionTreeRef"
        />
        <!-- 编辑权限对话框的确定和取消按钮 -->
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="handleClosePermission">取消</el-button>
            <el-button type="primary" @click="handleSubmitPermission"
              >确定</el-button
            >
          </div>
        </template>
      </el-dialog>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref, reactive, getCurrentInstance } from 'vue'

const instance = getCurrentInstance()
const { proxy } = instance

onMounted(() => {
  getRoleList()
})

// 获取菜单列表
const menuList = ref([])
const getMenuList = async () => {
  let params = { include_buttons: false }
  const res = await proxy.$api.getAllMenuList(params)
  menuList.value = res.data
}

// 控制是否显示新增角色的对话框
const showRoleForm = ref(false)

// 角色创建/编辑表单校验规则
const rules = reactive({
  name: [
    {
      required: true,
      message: '角色名称不能为空',
      trigger: 'blur',
    },
  ],
  code: [
    {
      required: true,
      message: '角色编码不能为空',
      trigger: 'blur',
    },
  ],
})

// 关闭创建菜单的表单（点击取消按钮时）
const handleClose = () => {
  // 使用resetFields方法重置表单
  proxy.$refs.roleFormRef.resetFields()
  showRoleForm.value = false
}

// 角色查询表单
const roleQueryForm = reactive({})
// 分页属性
const pager = reactive({
  page: 1, // 当前是第几页
  page_size: 10, // 一页多少条
})
// role列表查出来的总数，用于分页
const total = ref()
// roleList角色列表
const roleList = ref([])
// 重置按钮
const handleResetForm = () => {
  proxy.$refs.roleQueryFormRef.resetFields()
}

// 角色列表的列名称
const columns = reactive([
  { label: '角色名称', prop: 'name' },
  { label: '角色编码', prop: 'code' },
  {
    label: '关联菜单',
    prop: 'menu',
    formatter: (row) => {
      if (Array.isArray(row.menu)) {
        return row.menu.map((item) => item.title).join(', ')
      }
      return '-'
    },
  },
  { label: '备注', prop: 'remark' },
])

// 点击查询按钮时
const handleQuery = () => {
  getRoleList()
}
// 获取角色列表
const getRoleList = async () => {
  let params = { ...roleQueryForm, ...pager }
  let res = await proxy.$api.getRoleList(params)
  const { items, count } = res.data
  roleList.value = items
  total.value = count
}
// 分页事件，点击第几页时的处理函数
const handleCurrentChange = (current_page) => {
  // 将当前点击的第几页赋值给pager的page
  pager.page = current_page
  getRoleList()
}
// 分页事件，页码size改变时的处理函数
const handleSizeChange = (current_size) => {
  // 将当前点击的页码数量赋值给pager的page
  pager.page_size = current_size
  getRoleList()
}

// 点击【确定】按钮时，用来区分是编辑还是创建，分别调不同的方法
const isEditMode = ref(false)

// 新增角色
const handleCreateRole = () => {
  isEditMode.value = false
  showRoleForm.value = true
}

// 角色使用用的表单数据对象
const roleForm = reactive({})

// 点击编辑按钮时
const handleEdit = async (row) => {
  isEditMode.value = true
  showRoleForm.value = true

  let res = await proxy.$api.getRoleDetail(row.id)
  if (res && res.success) {
    roleForm.id = res.data.id
    roleForm.name = res.data.name
    roleForm.code = res.data.code
    roleForm.status = res.data.status
    roleForm.remark = res.data.remark
  }
}

// 新增、编辑角色时，提交给后台接口
const handleSubmit = () => {
  proxy.$refs.roleFormRef.validate(async (valid) => {
    if (valid) {
      let res
      try {
        // 创建模式
        if (!isEditMode.value) {
          res = await proxy.$api.createRole(roleForm)
          if (res && res.success) {
            proxy.$message.success('创建成功')
          }
        } else {
          // 编辑模式
          res = await proxy.$api.updateRole(roleForm)
          if (res && res.success) {
            proxy.$message.success('修改成功')
          }
        }
      } catch (error) {
        // console.log(error)
        proxy.$message.error('识别出错，可能是内容过多无法识别')
      } finally {
        if (res && res.success) {
          showRolePermission.value = false
          getRoleList()
          handleClose()
        }
      }
    }
  })
}

// 控制角色权限管理对话框是否显示
const showRolePermission = ref(false)
const permissionTreeProps = reactive({
  label: 'title', // 多选
})

// 当前编辑的这一行数据的id
const currentRowId = ref()

// 点击权限管理按钮时
const handlePermission = async (row) => {
  showRolePermission.value = true
  await getMenuList()
  let permissionList = []

  // 只把子菜单的id 设置为被选中的
  // 但是这里会有一个bug，当父菜单下没有子菜单时，选这个父菜单是无效的
  for (let item of row.menu) {
    if (item.parent != null) {
      permissionList.push(item.id)
    }
  }
  console.log('permissionList', permissionList)
  proxy.$refs.permissionTreeRef.setCheckedKeys(permissionList)
  // 保存当前被点击的这一行的id，方便后面使用
  currentRowId.value = row.id
}
// 点击删除按钮时
const handleDel = async (row) => {
  let res = await proxy.$api.deleteRole(row.id)
  if (res && res.success) {
    proxy.$message.success('删除成功')
    getRoleList()
  }
}
// 点击权限弹框的取消按钮时
const handleClosePermission = () => {
  showRolePermission.value = false
}
// 点击权限弹框的确定按钮时
const handleSubmitPermission = async () => {
  let keys = proxy.$refs.permissionTreeRef.getCheckedKeys()
  let halfKeys = proxy.$refs.permissionTreeRef.getHalfCheckedKeys()

  console.log('keys', keys)
  console.log('halfKeys', halfKeys)
  // 将全选和半选的全部给到后端
  let params = { menu_ids: keys.concat(halfKeys) }
  // console.log(params)
  let res
  try {
    res = await proxy.$api.assiginPerToRole(currentRowId.value, params)
  } catch (error) {
  } finally {
    if (res && res.success) {
      proxy.$message.success('权限修改成功')
      handleClosePermission()
      getRoleList()
    }
  }
}
</script>
