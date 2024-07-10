<template>
  <div class="exception">
    <img src="@/assets/images/404.png" />
    <el-button class="btn-home" @click="goHome"> 回首页 </el-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style lang="scss">
.exception {
  position: relative;
  img {
    width: 100%;
    height: 100vh;
  }
  .btn-home {
    position: fixed;
    bottom: 100px;
    left: 50%;
  }
}
</style>
