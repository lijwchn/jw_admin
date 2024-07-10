<template>
  <div class="welcome">
    <div class="content">
      <div class="sub-title">欢迎体验</div>
      <div class="title">通用后台管理系统</div>
      <div class="desc">- Vue3.0+ElementPlus打造通用后台管理系统</div>
    </div>
    <div class="img-container">
      <img src="../assets/images/welcome.png" alt="" />
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss">
.welcome {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: #fff;
  .content {
    .sub-title {
      font-size: 30px;
      line-height: 42px;
      color: #333;
    }
    .title {
      font-size: 40px;
      line-height: 62px;
      color: #409eff;
    }
    .desc {
      text-align: right; // 字体向右对齐
      font-size: 14px;
      line-height: 42px;
      color: #999;
    }
  }
  .img-container {
    width: 700px;
    height: auto;
    img {
      width: 100%;
      height: auto;
      // transform: scale(1); //缩放比例
    }
  }
}
</style>
