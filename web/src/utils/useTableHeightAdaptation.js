// 表格高度自适应
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

export function useTableHeightAdaptation(initialOffset) {
  const tableHeight = ref(window.innerHeight - initialOffset)
  const screenHeight = ref(window.innerHeight)

  const updateScreenHeight = () => {
    screenHeight.value = window.innerHeight
  }

  watch(screenHeight, (newVal) => {
    tableHeight.value = newVal - initialOffset
  })

  onMounted(() => {
    window.addEventListener('resize', updateScreenHeight)
  })
  // 组件挂载到节点上之前执行
  // 移除事件监听器，以避免内存泄漏和不必要的性能消耗
  onBeforeUnmount(() => {
    window.removeEventListener('resize', updateScreenHeight)
  })

  return {
    tableHeight,
  }
}
