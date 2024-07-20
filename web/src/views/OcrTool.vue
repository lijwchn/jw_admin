<template>
  <div class="pic-ocr">
    <el-card>
      <template #header>
        <div class="card-header">
          <span style="font-weight: bold"
            >基于百度开源项目 paddle-ocr 文字识别工具</span
          >
        </div>
      </template>
      <div class="card-content">
        <div class="input-container">
          <el-upload
            ref="uploadRef"
            class="pic-uploader"
            action="#"
            drag
            :auto-upload="false"
            accept=".png,.jpg"
            :on-change="handleChange"
            :file-list="fileList"
            :http-request="handleFileUpload"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div>点击上传文件 / 或者拖拽到这里</div>
            <div class="el-upload__tip">只支持jpg/png格式的文件</div>
          </el-upload>
          <el-button
            class="upload-button"
            type="primary"
            :loading="btnStatus"
            :disabled="fileList.length === 0"
            @click="submitUpload"
            >上传图片</el-button
          >
        </div>
        <div class="result-container">
          <el-input
            v-model="ocrResult"
            type="textarea"
            :autosize="{ minRows: 9, maxRows: 20 }"
            placeholder="识别结果（详细 Json 格式数据可以看F12控制台）
Tips：因服务器 cpu 算力太低，如长时间未出结果，那就是图片内容过多识别失败~~"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, getCurrentInstance } from 'vue'
import axios from 'axios'

const instance = getCurrentInstance()
const { proxy } = instance

const fileList = ref([]) // 存储文件列表
const ocrResult = ref('') // 接口返回的ocr结果
const btnStatus = ref(false) // 上传图片按钮loading状态
const uploadRef = ref(null) // 添加对upload组件的引用

const handleChange = (file, newFileList) => {
  // 如果文件类型不符合 jpg，png
  if (file.name.slice(-3) != 'jpg' && file.name.slice(-3) != 'png') {
    proxy.$message.error('上传文件只能是 jpg | png 格式')
    newFileList.pop() // 删除本次上传的文件
  }
  // 判断 > 1M
  else if (file.size > 1048576) {
    proxy.$message.warning(`您上传的 ${file.name} 大于1M，识别可能会失败`)
  }
  // 如果文件数量超过 1，则移除除了最后一个之外的所有文件
  if (newFileList.length > 1) {
    newFileList.splice(0, newFileList.length - 1)
  }
  console.log('newFileList', newFileList.length)
  fileList.value = newFileList
}

// 处理上传文件
const handleFileUpload = async (options) => {
  const { file } = options
  const formData = new FormData()
  formData.append('file', file)

  try {
    let res = await axios({
      method: 'post',
      url: 'http://106.52.59.119:8001/ocr/predict-by-file',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    if (res && res.data.code === 200) {
      let ocrData = res.data.data
      let extractedText = ''
      ocrData.forEach((block) => {
        block.forEach((item) => {
          extractedText += item[1][0] + '\n'
        })
      })
      ocrResult.value = extractedText
      proxy.$message.success('识别成功')
    }
    uploadRef.value.clearFiles()
    fileList.value = []
    btnStatus.value = false
  } catch (error) {
    console.error('Error uploading file:', error)
    if (error.response) {
      console.error('Response error data:', error.response.data)
    }
    proxy.$message.error('文件处理失败，cpu算力太低')
    uploadRef.value.clearFiles()
    fileList.value = []
    btnStatus.value = false
  }
}

// 点击上传图片按钮时
const submitUpload = () => {
  btnStatus.value = true
  proxy.$refs.uploadRef.submit()
}
</script>

<style scoped>
.pic-ocr {
  height: auto;
  .card-content {
    display: flex;
    .input-container {
      width: 30%;
      .pic-uploader {
        padding-right: 10px;
      }
    }
    .result-container {
      padding-left: 10px;
      width: 70%;
    }
  }
}
.el-card {
  width: 70%;
  margin: auto; /* 水平居中 */
}
.card-header {
  font-size: 20px;
  text-align: center;
}
</style>
