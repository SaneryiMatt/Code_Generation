<template>
  <transition name="fade">
    <div v-if="message" class="notification" :class="type">
      {{ message }}
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const message = ref('')
const type = ref<'success' | 'error'>('success')

const show = (msg: string, msgType: typeof type.value) => {
  message.value = msg
  type.value = msgType
  setTimeout(() => message.value = '', 3000)
}

// 暴露方法供全局使用
defineExpose({ show })
</script>

<style scoped lang="scss">
.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 12px 24px;
  border-radius: 4px;
  color: white;
  z-index: 1000;

  &.success {
    background: #52c41a;
  }

  &.error {
    background: #f5222d;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
