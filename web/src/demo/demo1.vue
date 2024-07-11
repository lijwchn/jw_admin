<script setup>
import { ref } from 'vue'

const count = ref(0)

const props = defineProps(['title'])

const clickMe = () => {
  console.log('haha')
}
</script>

<template>
  <el-button @click="count++">You clicked me {{ count }} times.</el-button>
  <span> {{ title }}</span>
  <el-button @click="clickMe">点我</el-button>
</template>
