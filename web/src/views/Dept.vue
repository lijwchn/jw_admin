<template>
  <div class="dept-manage">
    <div class="query-form">
      <el-form :inline="true" :model="deptQueryForm" ref="deptQueryFormRef">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="deptQueryForm.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="部门状态" prop="status">
          <el-select
            v-model="deptQueryForm.status"
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
        <el-button type="primary" @click="handleCreateDept">新增</el-button>
      </div>
      <div class="table-content">
        <el-table :data="deptList" border>
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
        :title="isEditMode ? '编辑部门' : '新增部门'"
        v-model="showDeptForm"
        :before-close="handleClose"
      >
        <el-form
          :model="deptForm"
          label-width="100px"
          ref="deptFormRef"
          :rules="rules"
        >
          <el-form-item label="部门名称" prop="name">
            <el-input v-model="deptForm.name" placeholder="请输入部门名称" />
          </el-form-item>
          <el-form-item label="部门负责人" prop="owner">
            <el-input v-model="deptForm.owner" placeholder="请输入负责人名称" />
          </el-form-item>
          <el-form-item label="负责人手机号" prop="phone">
            <el-input
              v-model="deptForm.phone"
              placeholder="请输入负责人手机号"
            />
          </el-form-item>
          <el-form-item label="负责人邮箱" prop="email">
            <el-input v-model="deptForm.email" placeholder="请输入负责人邮箱" />
          </el-form-item>
          <el-form-item label="角色状态" prop="status">
            <el-radio-group v-model="deptForm.status">
              <el-radio-button label="启用" :value="true"></el-radio-button>
              <el-radio-button label="停用" :value="false"></el-radio-button>
            </el-radio-group>
            <div style="padding-left: 40px">如果不选，默认为启用状态</div>
          </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="handleClose">取消</el-button>
            <el-button type="primary" @click="handleSubmit">确定</el-button>
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
  getDeptList()
})

// 角色查询表单
const deptQueryForm = reactive({})
// 分页属性
const pager = reactive({
  page: 1, // 当前是第几页
  page_size: 10, // 一页多少条
})

// dept列表查出来的总数，用于分页
const total = ref()

// 定义部门列表
const deptList = ref([])
// 获取部门列表
const getDeptList = async () => {
  let params = { ...deptQueryForm, ...pager }
  try {
    let res = await proxy.$api.getDeptList(params)
    const { items, count } = res.data
    deptList.value = items
    total.value = count
    return true
  } catch (error) {
    return false
  }
}

// 关闭创建菜单的表单（点击取消按钮时）
const handleClose = () => {
  // 使用resetFields方法重置表单
  proxy.$refs.deptFormRef.resetFields()
  showDeptForm.value = false
}

// 重置按钮
const handleResetForm = () => {
  // deptQueryFormRef在模板中通过ref定义了，就可以不用在script中显示声明
  proxy.$refs.deptQueryFormRef.resetFields()
}

// 角色列表的列名称
const columns = reactive([
  { label: '部门名称', prop: 'name' },
  { label: '部门负责人', prop: 'owner' },
  { label: '负责人电话', prop: 'phone' },
  { label: '负责人邮箱', prop: 'email' },
])

// 点击查询按钮时
const handleQuery = async () => {
  let res = await getDeptList()
  if (res) {
    proxy.$message.success('查询成功')
  }
}

// 分页事件，点击第几页时的处理函数
const handleCurrentChange = (current_page) => {
  // 将当前点击的第几页赋值给pager的page
  pager.page = current_page
  getDeptList()
}
// 分页事件，页码size改变时的处理函数
const handleSizeChange = (current_size) => {
  // 将当前点击的页码数量赋值给pager的page
  pager.page_size = current_size
  getDeptList()
}

// 点击【确定】按钮时，用来区分是编辑还是创建，分别调不同的方法
const isEditMode = ref(false)
// 控制是否显示新增部门的对话框
const showDeptForm = ref(false)

// 新增部门
const handleCreateDept = () => {
  isEditMode.value = false
  showDeptForm.value = true
}

// 部门使用用的表单数据对象
const deptForm = reactive({})

const rules = reactive({
  name: [
    {
      required: true,
      message: '部门名称不能为空',
      trigger: 'blur',
    },
  ],
  owner: [
    {
      required: true,
      message: '部门负责人不能为空',
      trigger: 'blur',
    },
  ],
})

// 点击编辑按钮时
const handleEdit = async (row) => {
  isEditMode.value = true
  showDeptForm.value = true
  currentRowId.value = row.id

  let res = await proxy.$api.getDeptDetial(row.id)
  if (res && res.success) {
    deptForm.name = res.data.name
    deptForm.owner = res.data.owner
    deptForm.phone = res.data.phone
    deptForm.email = res.data.email
    deptForm.status = res.data.status
  }
}

// 当前编辑的这一行数据的id
const currentRowId = ref()

// 新增、编辑部门时，提交给后台接口
const handleSubmit = () => {
  proxy.$refs.deptFormRef.validate(async (valid) => {
    if (valid) {
      let res
      try {
        // 创建模式
        if (!isEditMode.value) {
          res = await proxy.$api.createDept(deptForm)
          if (res && res.success) {
            proxy.$message.success('创建成功')
          }
        } else {
          // 编辑模式
          res = await proxy.$api.updateDept(currentRowId.value, deptForm)
          if (res && res.success) {
            proxy.$message.success('修改成功')
          }
        }
      } catch (error) {
        console.log(error)
      } finally {
        if (res && res.success) {
          getDeptList()
          handleClose()
        }
      }
    }
  })
}

// 点击删除按钮时
const handleDel = async (row) => {
  let res = await proxy.$api.deleteDept(row.id)
  if (res && res.success) {
    proxy.$message.success('删除成功')
    getDeptList()
  }
}
</script>
