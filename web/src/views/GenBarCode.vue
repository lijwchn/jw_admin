<template>
  <div class="gen-barcode-container">
    <div class="btn-inpput">
      <el-input
        type="textarea"
        class="input-area"
        :autosize="{ minRows: 8, maxRows: 16 }"
        placeholder="需要生成多个条形码请换行"
        v-model="inputContent"
      ></el-input>
      <el-button @click="genBarcodes" type="primary">生成条形码</el-button>
    </div>

    <div class="barcodes">
      <div
        class="barcode-warpper"
        v-for="(barcode, index) in barcodes"
        :key="index"
      >
        <svg :id="'barcode' + index"></svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import JsBarcode from 'jsbarcode'

const inputContent = ref('')
const barcodes = ref([])
const genBarcodes = () => {
  // 更新 barcodes 数组
  barcodes.value = inputContent.value
    .split('\n')
    .filter((line) => line.trim() !== '')

  // 等待 DOM 更新
  nextTick(() => {
    barcodes.value.forEach((barcode, index) => {
      JsBarcode(`#barcode${index}`, barcode, {
        format: 'CODE128',
        displayValue: true,
      })
    })
  })
}
</script>

<style lang="scss" scoped>
.gen-barcode-container {
  text-align: center; // 设置块元素行内内容水平对齐是居中显示
  background-color: #fff;
  .btn-inpput {
    display: flex;
    flex-wrap: nowrap;
    padding: 20px;
    .input-area {
      padding-right: 20px;
    }
  }
  .barcodes {
    display: flex;
    flex-wrap: wrap; // 换行显示
    justify-content: center;
    .barcode-warpper {
      display: flex;
      text-align: center;
      margin: 10px;
      width: calc(25% - 20px); /* 4个一行，减去margin */
      box-sizing: border-box;
    }
  }
}
</style>
