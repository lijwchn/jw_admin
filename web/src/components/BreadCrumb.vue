<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="item in breadList" :key="item.path">
      {{ item.meta.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script>
export default {
  name: 'BreadCrumb',
  computed: {
    breadList() {
      return this.$route.matched
    },
  },
}
</script>

<style></style>
