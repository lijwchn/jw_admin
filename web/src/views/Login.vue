<template>
  <div class="login-wrapper">
    <div class="model">
      <!-- :model="user" 登录的对象，包含帐号密码 -->
      <!-- status-icon 输入时会多一个状态图标 -->
      <!-- :rules 校验输入的账密规则，绑定的是 script 中的rules对象 -->
      <!-- ref="userFormRef"用在了 <el-form> 组件上,意味着可以通过 this.$refs.userFormRef 在 Vue 实例的方法中访问到这个 <el-form> 组件的实例 -->
      <!-- userFormRef 在这里绑定和在script中声明，效果是一样的 -->
      <el-form :model="user" status-icon :rules="rules" ref="userFormRef">
        <div class="title">火星</div>
        <!-- prop="userName" 需要加上这个，上面的校验规则 rules 才会生效 -->
        <el-form-item prop="username">
          <!-- v-model="user.username" 用于创建双向数据绑定 -->
          <el-input type="text" placeholder="帐号" v-model="user.username" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="密码"
            v-model="user.password"
            :show-password="true"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-btn" @click="login"
            >登录</el-button
          >
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data() {
    return {
      user: {
        username: '演示账号',
        password: '123456',
      },
      rules: {
        username: [
          {
            required: true,
            message: '请输入用户名',
            trigger: 'blur',
          },
        ],
        password: [
          {
            required: true,
            message: '请输入密码',
            trigger: 'blur',
          },
        ],
      },
    }
  },
  methods: {
    login() {
      this.$refs.userFormRef.validate((valid) => {
        if (valid) {
          this.$api.login(this.user).then((res) => {
            console.log('登录接口返回值', res)
            this.$store.commit('saveUserToken', 'Bearer ' + res.data.access)
            this.$store.commit('saveUserInfo', res.data.user_info)
            this.$router.push('/welcome')
          })
        } else {
          return
        }
      })
    },
  },
}
</script>

<style lang="scss">
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9fcff;
  width: 100vw;
  height: 100vh;
  .model {
    width: 500px;
    padding: 50px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0px 0px 10px 3px #c7c9cb4d; // 登录框周围的阴影框
    .title {
      font-size: 40px;
      line-height: 1.5; // 行间距
      text-align: center;
      margin-bottom: 30px; // 底部外边距
    }
    .login-btn {
      width: 100%;
    }
  }
}
</style>
