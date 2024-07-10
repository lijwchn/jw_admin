<template>
  <div class="barcode-container">
    <div class="barcodes">
      <div
        v-for="(barcode, index) in barcodes"
        :key="index"
        class="barcode-wrapper"
      >
        <svg :id="'barcode' + index"></svg>
      </div>
    </div>
    <el-button @click="fetchBarcodes" type="primary"
      >通过接口获取条形码</el-button
    >
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'
import JsBarcode from 'jsbarcode'

const instance = getCurrentInstance()
const { proxy } = instance

const barcodes = ref([])

const fetchBarcodes = async () => {
  let res = await proxy.$api.createOrder()
  if (res && res.success) {
    barcodes.value = res.data
    proxy.$nextTick(() => {
      barcodes.value.forEach((barcode, index) => {
        // 生成类似于 #barcode0、#barcode1 这样的字符串
        // 作为参数传递给 JsBarcode 函数，告诉它要操作哪个 SVG 元素来绘制条形码
        JsBarcode(`#barcode${index}`, barcode, {
          format: 'CODE128',
          displayValue: true,
        })
      })
    })
  }
}
</script>

<style lang="scss" scoped>
.barcode-container {
  text-align: center; // 设置块元素行内内容水平对齐是居中显示
  background-color: #fff;
}
button {
  margin-bottom: 20px;
  margin-top: 20px;
}
.barcodes {
  display: flex;
  flex-wrap: wrap; // 换行显示
  justify-content: center;
  .barcode-wrapper {
    display: flex;
    align-items: center;
    margin: 10px;
    width: calc(25% - 20px); /* 4个一行，减去margin */
    box-sizing: border-box;
  }
}
</style>
