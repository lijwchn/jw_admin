<template>
  <!-- 导航菜单 -->
  <!-- router="true" 可以把index作为路由直接跳转 -->
  <el-menu
    class="nav-menu"
    :router="true"
    background-color="#001529"
    text-color="#fff"
  >
    <template v-for="menu in userMenuList">
      <el-sub-menu
        v-if="menu.children && menu.children.length"
        :index="menu.path"
        :key="menu.id"
      >
        <template #title>
          <el-icon>
            <component :is="menu.icon" />
          </el-icon>
          <span>{{ menu.title }}</span>
        </template>
        <el-menu-item
          v-for="child in menu.children"
          :index="child.path"
          :key="child.id"
        >
          {{ child.title }}
        </el-menu-item>
      </el-sub-menu>
    </template>
  </el-menu>
</template>

<script>
export default {
  name: 'MenuTree',
  props: {
    userMenuList: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style></style>
