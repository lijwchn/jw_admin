<script setup>
import ButtonCounter from '@/demo/demo1.vue'

const clickMe2 = () => {
  console.log('xixi')
}
</script>

<template>
  <h1>Here is a child component!</h1>
  <ButtonCounter title="haha1" />
  <ButtonCounter title="haha2" />
</template>
