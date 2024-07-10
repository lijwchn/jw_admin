<template>
  <div class="menu-manage">
    <div class="query-form">
      <el-form :inline="true" :model="menuQueryForm" ref="menuQueryFormRef">
        <el-form-item label="菜单状态" prop="status">
          <el-select
            v-model="menuQueryForm.status"
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
          <el-button @click="handleResetForm(menuQueryFormRef)">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="base-table">
      <!-- 操作按钮区域 -->
      <div class="action">
        <el-button type="primary" @click="handleCreateMenu">新增</el-button>
      </div>
      <div class="table-content">
        <el-table :data="menuList" row-key="id" border default-expand-all>
          <el-table-column
            v-for="item in columns"
            :key="item.id"
            :prop="item.prop"
            :label="item.label"
            :formatter="item.formatter"
          >
          </el-table-column>
          <el-table-column label="菜单状态">
            <template #default="scope">
              <el-tag :type="getTagType(scope.row.status)">
                {{ scope.row.status ? '启用' : '停用' }}
              </el-tag>
            </template>
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
    </div>
    <!-- v-model:控制是否显示这个dialog -->
    <el-dialog
      :title="isEditMode ? '编辑菜单' : '新增菜单'"
      v-model="showMenuForm"
      :before-close="handleClose"
    >
      <el-form
        :model="menuForm"
        label-width="100px"
        ref="menuFormRef"
        :rules="rules"
      >
        <el-form-item label="父级菜单" prop="parent_id">
          <el-cascader
            v-model="menuForm.parent_id"
            :options="menuList"
            :props="cascaderProps"
            clearable
          />
          <span style="margin-left: 20px"> 如果不选，则直接创建一级菜单</span>
        </el-form-item>
        <el-form-item label="菜单类型" prop="type">
          <el-radio-group v-model="menuForm.type">
            <el-radio-button label="一级" :value="1"></el-radio-button>
            <el-radio-button label="二级" :value="2"></el-radio-button>
            <!-- <el-radio label="按钮" :value="3"></el-radio> -->
          </el-radio-group>
        </el-form-item>
        <el-form-item label="菜单名称" prop="title">
          <el-input v-model="menuForm.title" placeholder="请输入菜单名称" />
        </el-form-item>
        <el-form-item
          label="菜单图标"
          prop="icon"
          v-if="menuForm.type == 1 ? true : false"
        >
          <el-input
            placeholder="请输入菜单图标(仅一级菜单需要)"
            v-model="menuForm.icon"
          />
        </el-form-item>
        <el-form-item label="路由地址" prop="path">
          <el-input placeholder="请输入菜单路由地址" v-model="menuForm.path" />
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input
            placeholder="请输入菜单排序，只能是数字"
            v-model="menuForm.order"
            type="number"
          />
        </el-form-item>
        <el-form-item label="菜单状态" prop="status">
          <el-radio-group v-model="menuForm.status">
            <el-radio-button label="启用" :value="true"></el-radio-button>
            <el-radio-button label="停用" :value="false"></el-radio-button>
          </el-radio-group>
          <div style="padding-left: 40px">如果不选，默认为启用状态</div>
        </el-form-item>
      </el-form>
      <!-- #footer 指定确定取消是在footer区域 -->
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClose">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, getCurrentInstance } from 'vue'

const instance = getCurrentInstance()
const { proxy } = instance

onMounted(() => {
  getMenuList()
})

// 查询菜单时，接口请求的数据
const menuQueryForm = reactive({})
// 查询菜单时的表单
const menuQueryFormRef = ref(null)
// 菜单列表
const menuList = ref([])

const getMenuList = async () => {
  menuQueryForm.include_buttons = false
  let params = { ...menuQueryForm }
  const res = await proxy.$api.getAllMenuList(params)
  menuList.value = res.data
}
// 查询按钮
const handleQuery = () => {
  getMenuList()
}
// 重置按钮
const handleResetForm = (formRef) => {
  formRef.resetFields()
}

// 渲染菜单的列数据
const columns = reactive([
  { label: '菜单名称', prop: 'title' },
  // { label: '图标', prop: 'icon' },
  { label: '路径', prop: 'path' },
  {
    label: '类型',
    prop: 'type',
    formatter(row, column, value) {
      return {
        1: '一级菜单',
        2: '二级菜单',
        3: '按钮',
      }[value]
    },
  },
  { label: '排序', prop: 'order' },
])

// 控制是否显示新增菜单的对话框
const showMenuForm = ref(false)

// 新增菜单时，使用的表单数据对象
const menuForm = reactive({})
// 级联选择器配置项
const cascaderProps = {
  expandTrigger: 'hover',
  // 取字段中的title作为标签在选择器中显示
  label: 'title',
  value: 'id',
  // 可选择任意一级
  checkStrictly: true,
}

// 点击新增菜单按钮时
const handleCreateMenu = () => {
  isEditMode.value = false
  showMenuForm.value = true
  getMenuList()
}

// 菜单创建/编辑表单校验规则
const rules = reactive({
  type: [
    {
      required: true,
      message: '菜单类型不能为空',
      trigger: 'blur',
    },
  ],
  title: [
    {
      required: true,
      message: '菜单名称不能为空',
      trigger: 'blur',
    },
    {
      min: 2,
      max: 8,
      message: '菜单名称必须在2-8字符',
    },
  ],
  path: [
    {
      required: true,
      message: '路由地址不能为空',
      trigger: 'blur',
    },
  ],
  order: [
    {
      required: true,
      message: '菜单排序不能为空',
      trigger: 'blur',
    },
  ],
})

// 判断是编辑模式还是创建模式
const isEditMode = ref(false)

// 点击确定按钮时
const handleSubmit = () => {
  proxy.$refs.menuFormRef.validate(async (valid) => {
    if (valid) {
      let res
      try {
        // 创建模式
        if (!isEditMode.value) {
          res = await proxy.$api.createMenu(menuForm)
          if (res.success) {
            proxy.$message.success('创建成功')
          } else {
            proxy.$message.error('创建失败')
          }
        } else {
          // 编辑模式
          // debugger
          res = await proxy.$api.updateMenu(menuForm)
          if (res.success) {
            proxy.$message.success('修改成功')
          } else {
            proxy.$message.error('修改失败')
          }
        }
      } catch (error) {
        console.error(error)
        // proxy.$message.error('请求失败')
      } finally {
        if (res && res.success) {
          showMenuForm.value = false
          getMenuList()
          handleClose()
        }
      }
    }
  })
}

// 点击编辑按钮时
const handleEdit = async (row) => {
  isEditMode.value = true
  showMenuForm.value = true
  getMenuList()

  let res = await proxy.$api.getMenuDetialById(row.id)
  // debugger
  if (res && res.success) {
    // 将接口返回的parent_id从数字处理成数组
    menuForm.parent_id = ref([])
    if (res.data.parent) {
      menuForm.parent_id.push(res.data.parent)
      // menuForm.parent_id.push(res.data.id)
    }

    if (res.data.icon) {
      menuForm.icon = res.data.icon
    }
    menuForm.order = res.data.order
    menuForm.path = res.data.path
    menuForm.title = res.data.title
    menuForm.type = res.data.type
    menuForm.id = res.data.id
  }
}

// 关闭创建菜单的表单（点击取消按钮时）
const handleClose = () => {
  // 使用resetFields方法重置表单
  proxy.$refs.menuFormRef.resetFields()
  showMenuForm.value = false
}

// 获取菜单状态的图标类型
const getTagType = (status) => {
  return status ? 'success' : 'danger'
}

// 点击确认删除按钮时
const handleDel = async (row) => {
  let res = await proxy.$api.deleteMenu(row.id)
  if (res.success) {
    proxy.$message.success('删除成功')
    getMenuList()
  }
}
</script>

<style lang="scss"></style>
