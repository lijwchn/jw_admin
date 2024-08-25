<template>
  <div class="basic-layout">
    <!-- 左侧导航栏 -->
    <!-- :class vue中的动态属性绑定，如果收起导航栏（isCollapes=true）,则fold=60px -->
    <div :class="['nav-side', isCollapes ? 'fold' : 'unfold']">
      <!-- 系统logo -->
      <div class="logo" @click="goHome">
        <img src="./../assets/logo.png" />
        <span>JW-admin</span>
      </div>
      <!-- :collapse="isCollapes" 控制是否收起导航栏，和点击事件 toggle 绑定 -->
      <!-- :default-active="activeMenu" 控制默认选中的菜单（高亮） -->
      <TreeMenu
        :collapse="isCollapes"
        :default-active="activeMenu"
        :userMenuList="userMenuList"
      />
    </div>
    <!-- 右侧全部内容区域 -->
    <div :class="['content-right', isCollapes ? 'fold' : 'unfold']">
      <!-- 右侧上部导航栏 -->
      <div class="nav-top">
        <!-- 面包屑和收起导航栏的区域 -->
        <div class="nav-left">
          <div class="menu-fold" @click="toggle">
            <el-icon><Fold /></el-icon>
          </div>
          <div class="bread">
            <BreadCrumb />
          </div>
        </div>
        <div class="user-info">
          <el-badge :is-dot="this.showDot" class="notice">
            <el-icon><Bell /></el-icon>
          </el-badge>
          <el-dropdown @command="handleCommand">
            <span class="user-link">
              {{ userInfo.username }}
              <el-icon>
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="email"
                  >邮箱：{{ userInfo.email }}</el-dropdown-item
                >
                <el-dropdown-item command="changePassword"
                  >修改密码</el-dropdown-item
                >
                <el-dropdown-item command="logout">退出</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      <!-- 右侧内容区域 -->
      <div class="wrapper">
        <router-view></router-view>
      </div>
    </div>
  </div>
  <el-dialog title="修改密码" v-model="showChangePasswordForm" width="500">
    <el-form
      :model="changePasswordForm"
      :rules="rules"
      ref="changePasswordFormRef"
    >
      <el-form-item label="帐号" prop="username">
        <el-input
          v-model="changePasswordForm.username"
          placeholder="请输入用户名"
        ></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          type="password"
          :show-password="true"
          v-model="changePasswordForm.password"
          placeholder="请输入密码"
        ></el-input>
      </el-form-item>
    </el-form>
    <!-- #footer 指定确定取消是在footer区域 -->
    <template #footer>
      <div class="dialog-footer">
        <!-- <el-button @click="handleClose">取消</el-button> -->
        <el-button type="primary" @click="changePassword">确定</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import TreeMenu from './TreeMenu.vue'
import BreadCrumb from './BreadCrumb.vue'

export default {
  name: 'Home',
  components: { TreeMenu, BreadCrumb },
  data() {
    return {
      userInfo: this.$storage.getItem('userInfo') || {},
      // userInfo: this.$store.state.userInfo || {},
      isCollapes: false,
      showDot: false,
      userMenuList: [],
      // 截取路由地址，赋值给当前选中的菜单
      activeMenu: location.hash.slice(1),

      //修改密码相关变量
      showChangePasswordForm: false,
      changePasswordForm: {},
      rules: {
        username: [
          {
            required: true,
            message: '用户名不能为空',
            trigger: 'blur',
          },
        ],
        password: [
          {
            required: true,
            message: '密码不能为空',
            trigger: 'blur',
          },
        ],
      },
    }
  },
  mounted() {
    this.getNoticeCount()
    this.getUserMenuPermission()
    this.changePasswordForm.username = this.userInfo.username
    // console.log('home页面', this.$api.getUserList)
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    // 处理登出
    handleCommand(key) {
      if (key === 'logout') {
        // 清空用户信息,跳到登录页面
        this.$store.commit('saveUserToken', '')
        this.userToken = null
        this.$router.push('/login')
      }
      if (key === 'changePassword') {
        this.showChangePasswordForm = true
      }
    },
    // 处理是否收起导航栏
    toggle() {
      this.isCollapes = !this.isCollapes
    },
    async getNoticeCount() {
      try {
        const res = await this.$api.getNoticeCount()
        if (res.data > 0) {
          this.showDot = true
        }
        console.log('通知数量--->', res.data)
      } catch (error) {
        console.log(error)
      }
    },
    // 获取菜单列表
    async getUserMenuPermission() {
      try {
        const res = await this.$api.getUserMenuPermission()
        this.userMenuList = res.data
      } catch (error) {
        console.log(error)
      }
    },
    // 修改密码
    changePassword() {
      this.$refs.changePasswordFormRef.validate(async (valid) => {
        if (valid) {
          let res
          try {
            res = await this.$api.changePassword(this.changePasswordForm)
            if (res && res.success) {
              this.$message.success('密码修改成功')
            }
          } catch (error) {
          } finally {
            if (res && res.success) {
              this.showChangePasswordForm = false
            }
          }
        }
      })
    },
  },
}
</script>

<style lang="scss">
// 覆盖 el-dropdown 组件出现的这个样式（当鼠标放在上面出现）
:focus-visible {
  outline: none;
}
.basic-layout {
  position: relative;
  .nav-side {
    // 当左侧导航栏收起时
    &.fold {
      width: 60px;
    }
    // 当左侧导航栏展开时
    &.unfold {
      width: 200px;
    }
    position: fixed;
    // width: 200px;
    height: 100vh;
    background-color: #001529;
    color: #fff; // 字体颜色
    overflow: auto; // 默认显示 y 轴方向的滑动条
    transition: width 0.2s; // 收起左侧导航栏时的动画效果
    .nav-menu {
      // 导航栏的高度，当导航栏过高时，不会出现在页面之外
      height: calc(100vh - 50px);
      // 不要导航栏的右边框
      border-right: none;
    }
    .logo {
      display: flex;
      align-items: center;
      font-size: 18px;
      height: 50px;
      img {
        margin: 0 16px;
        width: 32px;
        height: auto;
      }
    }
  }
  .content-right {
    // 当左侧导航栏收起时
    &.fold {
      margin-left: 60px;
    }
    // 当左侧导航栏展开时
    &.unfold {
      margin-left: 200px;
    }
    // margin-left: 200px;
    .nav-top {
      height: 50px;
      line-height: 50px;
      display: flex;
      justify-content: space-between; // 两头对齐
      border-bottom: 1px solid #ddd;
      padding: 0 20px;
      .nav-left {
        display: flex;
        align-items: center;
        .menu-fold {
          padding-top: 7px;
        }
        .bread {
          padding-left: 10px;
        }
      }
      .user-info {
        .notice {
          line-height: 30px;
        }
        .user-link {
          padding-top: 14px;
          padding-left: 15px;
          font-size: 15px;
        }
      }
    }
    .wrapper {
      background: #eef0f3;
      padding: 10px;
      height: calc(100vh - 50px);
    }
  }
}
</style>
