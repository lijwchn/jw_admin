<template>
  <div class="user-manage">
    <div class="query-form">
      <!-- :inline="true" 设置为横着排列 -->
      <!-- :model="userForm" 绑定这个表单的对象为 userForm，方便里面的组件取值 v-bind:model的简写 -->
      <el-form :inline="true" :model="userForm" ref="userFormRef">
        <el-form-item label="用户名" prop="username">
          <!-- v-model="userForm.username" 是双向绑定 -->
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="电话" prop="mobile">
          <el-input v-model="userForm.mobile" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="部门" prop="dept_id">
          <el-select
            v-model="userForm.dept_id"
            clearable
            placeholder="选择部门"
            style="width: 150px"
          >
            <el-option
              v-for="item in deptList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
            v-model="userForm.status"
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
          <el-button @click="handleResetForm(userFormRef)">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="base-table">
      <!-- 操作按钮区域 -->
      <div class="action">
        <el-button type="primary" @click="handleCreate">新增</el-button>
        <el-button type="danger" @click="batchDelUser">批量删除</el-button>
      </div>
      <div class="table-content">
        <!-- 表格数据区域 -->
        <el-table
          :data="userList"
          @selection-change="handleSelectionChange"
          border
          :height="tableHeight"
        >
          <!-- 第一列是复选框 -->
          <el-table-column type="selection" width="55" />
          <el-table-column
            v-for="item in columns"
            :key="item.prop"
            :prop="item.prop"
            :label="item.label"
            :formatter="item.formatter"
          />
          <el-table-column label="用户状态">
            <template #default="rowContent">
              <el-tag :type="getTagType(rowContent.row.status)">
                {{ rowContent.row.status ? '启用' : '停用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="100">
            <!-- #default="rowContent" 表示当前行的数据 -->
            <template #default="rowContent">
              <el-button size="small" @click="editUser(rowContent.row)"
                >编辑</el-button
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
    </div>
    <!-- v-model:控制是否显示这个dialog -->
    <el-dialog
      :title="isEditMode ? '编辑用户' : '新增用户'"
      v-model="showUserForm"
      :before-close="handleClose"
    >
      <!-- ref="userCreateFormRef" 个人理解，不写ref属性也能校验，但是最终提交的时候，一般需要 $refs.userCreateFormRef.validate 验证有效才行 -->
      <el-form
        :model="userCreateForm"
        label-width="100px"
        :rules="rules"
        ref="userCreateFormRef"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="userCreateForm.username"
            placeholder="请输入用户名"
            :disabled="isEditMode"
          />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userCreateForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userCreateForm.email" placeholder="请输入用户邮箱">
            <!-- <template #append>@qq.com</template> -->
          </el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="mobile">
          <el-input
            v-model="userCreateForm.mobile"
            placeholder="请输入手机号"
          />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="userCreateForm.gender">
            <el-radio-button label="男" :value="1" />
            <el-radio-button label="女" :value="0" />
          </el-radio-group>
        </el-form-item>
        <el-form-item label="部门" prop="dept_id">
          <el-select v-model="userCreateForm.dept_id" placeholder="选择部门">
            <el-option
              v-for="item in deptList"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="角色" prop="role_ids">
          <el-select
            v-model="userCreateForm.role_ids"
            placeholder="选择角色"
            multiple
          >
            <el-option
              v-for="item in roleList"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <!-- #footer 指定确定取消是在footer区域 -->
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClose">取消</el-button>
          <el-button type="primary" @click="handleConfirm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, getCurrentInstance } from 'vue'
import { useTableHeightAdaptation } from '@/utils/useTableHeightAdaptation.js'

const instance = getCurrentInstance()
const { proxy } = instance

// reactive一般用来定义引用类型,ref一般定义基本类型
const userForm = reactive({})

const columns = reactive([
  { label: '用户名', prop: 'username' },
  { label: '姓名', prop: 'name' },
  {
    label: '性别',
    prop: 'gender',
    formatter(value) {
      return {
        0: '女',
        1: '男',
      }[value.gender]
    },
  },
  { label: '电话', prop: 'mobile' },
  { label: '邮箱', prop: 'email' },
  { label: '部门', prop: 'dept.name' },
  // {
  //   label: '状态',
  //   prop: 'status',
  //   formatter(row, column, value) {
  //     return {
  //       false: '停用',
  //       true: '启用',
  //     }[value]
  //   },
  // },
])
// 用户列表
const userList = ref([])
// 分页属性
const pager = reactive({
  page: 1, // 当前是第几页
  page_size: 10, // 一页多少条
})
// user列表查出来的总数，用于分页
const total = ref()
// 表单校验规则
const rules = reactive({
  username: [
    {
      required: true,
      message: '用户名不能为空',
      trigger: 'blur',
    },
  ],
  name: [
    {
      required: true,
      message: '姓名不能为空',
      trigger: 'blur',
    },
  ],
})

onMounted(() => {
  getUserList()
  getDeptList()
})

const getUserList = async () => {
  let params = { ...userForm, ...pager }
  try {
    let res = await proxy.$api.getUserList(params)
    const { items, count } = res.data
    total.value = count
    userList.value = items
    return true
  } catch (error) {
    return false
  }
}
// 查询用户时的表单
const userFormRef = ref(null)
// 查询按钮
const handleQuery = async () => {
  let res = await getUserList()
  if (res) {
    proxy.$message.success('查询成功')
  }
}
// 重置按钮
const handleResetForm = (formRef) => {
  formRef.resetFields()
}

// 获取用户状态的图标类型
const getTagType = (status) => {
  return status ? 'success' : 'danger'
}

// 分页事件，点击第几页时的处理函数
const handleCurrentChange = (current_page) => {
  // 将当前点击的第几页赋值给pager的page
  pager.page = current_page
  getUserList()
}
// 分页事件，页码size改变时的处理函数
const handleSizeChange = (current_size) => {
  // 将当前点击的页码数量赋值给pager的page
  pager.page_size = current_size
  getUserList()
}
// 删除按钮
const handleDel = async (row) => {
  await proxy.$api.deleteUser({
    ids: [row.id],
  })
  proxy.$message.success('删除成功')
  getUserList()
}

// 批量删除按钮
const batchDelUser = async () => {
  if (checkSelectionChange.value.length == 0) {
    proxy.$message.success('请选择要删除的用户')
    return
  }
  await proxy.$api.deleteUser({
    ids: checkSelectionChange.value,
  })
  proxy.$message.success('删除成功')
  getUserList()
}

// 处理表格多选
const checkSelectionChange = ref([])

const handleSelectionChange = (selectList) => {
  let arr = []
  selectList.map((item) => {
    arr.push(item.id)
  })
  checkSelectionChange.value = arr
}

// 新增用户时，使用的表单数据对象
const userCreateForm = reactive({})
// 控制是否显示新增用户的form
const showUserForm = ref(false)
// 新增用户时，表单的字段
// const userCreateFormRef = ref()
// 新增用户
const handleCreate = () => {
  // 设置为非编辑模式
  isEditMode.value = false

  // 打开用户弹框
  showUserForm.value = true
  getDeptList()
  getRoleList()
}

// 存储部门数据
const deptList = ref([])
// 获取部门数据
const getDeptList = async () => {
  let res = await proxy.$api.getDeptList()
  deptList.value = res.data.items
}
// 存储角色数据
const roleList = ref([])
// 获取所有角色数据
const getRoleList = async () => {
  let res = await proxy.$api.getRoleList({ status: true })
  roleList.value = res.data.items
}

// 点击【确定】按钮时，用来区分是编辑还是创建，分别调不同的方法
const isEditMode = ref(false)
// 提交创建、编辑 用户的表单
const handleConfirm = () => {
  proxy.$refs.userCreateFormRef.validate(async (valid) => {
    if (valid) {
      let res
      try {
        // 创建模式
        if (isEditMode.value === false) {
          res = await proxy.$api.createUser(userCreateForm)
          if (res && res.success) {
            proxy.$message.success('用户创建成功')
          }
        } else if (isEditMode.value === true) {
          // 编辑模式
          res = await proxy.$api.updateUserInfo(userCreateForm)
          if (res && res.success) {
            proxy.$message.success('用户编辑成功')
          }
        }
      } catch (error) {
      } finally {
        // debugger
        if (res && res.success) {
          handleClose()
          setTimeout(getUserList, 500)
        }
      }
    }
  })
}
// 创建/编辑用户的表单关闭时
const handleClose = () => {
  console.log('前', userCreateForm)
  proxy.$refs.userCreateFormRef.resetFields()
  showUserForm.value = false
  console.log('后', userCreateForm)
}
// 编辑用户
const editUser = async (row) => {
  // 设置为编辑模式
  isEditMode.value = true
  // 打开弹框
  showUserForm.value = true
  getDeptList()
  getRoleList()

  let res = await proxy.$api.getUserDetailById(row.id)
  if (res && res.success) {
    // 给 userCreateForm 赋值
    userCreateForm.id = res.data.id
    userCreateForm.username = res.data.username
    userCreateForm.name = res.data.name
    userCreateForm.email = res.data.email ?? null
    userCreateForm.mobile = res.data.mobile ?? null
    userCreateForm.gender = res.data.gender ?? null
    userCreateForm.dept_id = res.data.dept?.id ?? null
    userCreateForm.role_ids = res.data.role?.map((item) => item.id) ?? []
  }
}
// 表格高度
const { tableHeight } = useTableHeightAdaptation(260)
</script>

<style lang="scss"></style>
