<template>
  <div class="codegen-app">
    <!-- 主内容区 -->
    <main class="app-main">
      <!-- 步骤1：需求输入 -->
      <div v-if="store.currentStep === 1" class="input-section">
        <h2>请详细描述您的功能，AI为您写代码</h2>
        <div class="input-container">
          <div class="textarea-wrapper">
            <textarea
              v-model="store.userInput"
              placeholder="例如：创建一个学生管理系统，包含姓名、学号、性别、班级等字段"
              @keydown.enter.prevent="handleEnter"
            ></textarea>
            <button
              class="optimize-btn"
              @click="optimizeText"
              :disabled="!store.userInput.trim() || store.isOptimizing"
            >
              <span v-if="store.isOptimizing">
                <i class="loading-icon"></i> 优化中...
              </span>
              <span v-else>🔍 语言优化</span>
            </button>
          </div>
          <div class="examples">
            <h3>示例需求：</h3>
            <ul>
              <li @click="fillExample('创建一个用户管理系统，包含登录、注册、权限管理功能')">
                用户管理系统
              </li>
              <li @click="fillExample('设计商品库存模型，包含SKU、库存数量、仓库位置')">
                商品库存模型
              </li>
            </ul>
          </div>
        </div>
        <button
          class="next-btn"
          @click="startGeneration"
          :disabled="!store.userInput.trim()"
        >
          开始生成 →
        </button>
      </div>

      <!-- 步骤2：代码生成中 -->
      <div v-else-if="store.currentStep === 2" class="generation-section">
        <div class="status-info">
          <div class="module-tag">{{ store.currentModule }}</div>
          <div class="status-message">
            {{ store.generationStatus }}
            <span class="dots">
              <span :class="{ active: store.dot1 }">.</span>
              <span :class="{ active: store.dot2 }">.</span>
              <span :class="{ active: store.dot3 }">.</span>
            </span>
          </div>
        </div>

        <!-- 显示生成的代码 -->
        <div class="code-display">
          <HighlightCode :code="store.generatedCode" :language="store.language" />
        </div>

        <div class="action-buttons">
          <button class="cancel-btn" @click="cancelGeneration" v-if="store.isGenerating">
            取消生成
          </button>
          <button class="view-btn" @click="showFullCode" :disabled="!store.generatedCode.length">
            {{ store.isGenerating ? '生成中...' : '查看完整代码 →' }}
          </button>
        </div>
      </div>
    </main>

    <!-- 全局通知 -->
    <Transition name="fade">
      <div v-if="store.notification.show" class="notification" :class="store.notification.type">
        {{ store.notification.message }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCodeGenStore } from '@/stores/codegen'
import HighlightCode from '@/components/HighlightCode.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useCodeGenStore()

// 填充示例
const fillExample = (example) => {
  store.setUserInput(example)
  store.showNotification('示例已填充，可点击"语言优化"或直接生成', 'info')
}

// 语言优化
const optimizeText = async () => {
  await store.optimizeText()
}

// 开始生成代码
const startGeneration = () => {
  store.startGeneration()
}

// 取消生成
const cancelGeneration = () => {
  store.cancelGeneration()
}

// 查看完整代码
const showFullCode = () => {
  router.push('/result')
}

// 回车键处理
const handleEnter = () => {
  if (store.userInput.trim()) {
    startGeneration()
  }
}

// 初始化
onMounted(() => {
  store.initState()
})
</script>

<style scoped lang="scss">
/* 样式保持不变，使用你提供的样式 */
</style>
