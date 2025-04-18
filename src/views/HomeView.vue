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
          <!-- 保留按钮而不显示进度和百分比 -->
          <div class="status-message">
            {{ store.generationStatus }}
            <span class="dots">
              <span :class="{ active: store.dot1 }">.</span>
              <span :class="{ active: store.dot2 }">.</span>
              <span :class="{ active: store.dot3 }">.</span>
            </span>
          </div>
        </div>

        <!-- 只显示生成的代码，而不显示进度条 -->
        <div class="code-display" ref="codeContainer" v-html="renderedMarkdown"></div>

        <div class="action-buttons">
          <!-- 取消生成按钮 -->
          <button class="cancel-btn" @click="cancelGeneration" >
            取消生成
          </button>
          <!-- 查看完整代码按钮 -->
          <button
            class="view-btn"
            @click="showFullCode"
            :disabled="store.progress < 100"
          >
            {{ store.progress < 100 ? '生成中...' : '查看完整代码 →' }}
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
import { ref, onMounted, watch, nextTick, computed } from 'vue'
import { useCodeGenStore } from '@/stores/codegen'
import HighlightCode from '@/components/HighlightCode.vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'

const router = useRouter()
const store = useCodeGenStore()
const codeContainer = ref(null)

const renderedMarkdown = computed(() => {
  return marked(store.generatedCode)  // 将生成的代码转换为HTML
})

// 自动滚动到底部
watch(() => store.generatedCode, () => {
  nextTick(() => {
    if (codeContainer.value) {
      codeContainer.value.scrollTop = codeContainer.value.scrollHeight
    }
  })
})

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
const startGeneration = async () => {
  store.setCurrentStep(2)  // 设置为第二步（代码生成）
  store.startGeneration()
  //router.push('/result')
  //await store.loadFilesFromStream('stream/code')

  // 跳转到结果页面

}

// 取消生成
const cancelGeneration = () => {
  store.setCurrentStep(1)  // 设置为第一步（需求输入）
  currentStep.value = 1
}

// 查看完整代码
const showFullCode = async () => {
  router.push('/result')
  await store.loadFlaskFilesByPath()
  //await store.loadFilesFromStream('stream/code')
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

.textarea-wrapper textarea {
  caret-color: #1890ff;  /* 设置光标颜色 */
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  padding: 10px;
  width: 100%;
  min-height: 150px;
  resize: vertical;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  transition: border-color 0.3s;
  outline: none; /* 移除默认的轮廓 */
  white-space: pre-wrap; /* 处理换行 */
  word-wrap: break-word; /* 允许单词自动换行 */
}

/* 增加textarea的背景和光标颜色 */
.textarea-wrapper textarea:focus {
  outline: none;
  border-color: #dc18ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.textarea-wrapper textarea::selection {
  background-color: #1890ff;
  color: white;
}

.textarea-wrapper textarea {
  color: #333;
}


/* 生成代码显示区域 */
.code-display {
  background: #f8f8f8;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  max-height: 400px; /* 设置最大高度 */
  overflow-y: auto; /* 允许垂直滚动 */
  font-family: monospace;
  white-space: pre-wrap; /* 处理换行 */
  word-wrap: break-word; /* 允许单词自动换行 */
  overflow-wrap: break-word; /* 保证长单词换行 */
  max-width: 100%; /* 宽度自动适应，避免过宽 */
  width: 100%; /* 使代码区域自适应宽度 */
  border: 1px solid #e8e8e8;

  code {
    display: block;
    line-height: 1.5;
  }
}

/* 基础样式 */
.codegen-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
}

.app-header {
  background-color: #304156;
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
  }
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

/* 输入区域样式 */
.input-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.input-container {
  margin-bottom: 1.5rem;
}

.textarea-wrapper {
  position: relative;
  margin-bottom: 1rem;

  textarea {
    width: 100%;
    min-height: 150px;
    padding: 1rem;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    font-family: inherit;
    font-size: 1rem;
    resize: vertical;
    transition: border-color 0.3s;

    &:focus {
      outline: none;
      border-color: #1890ff;
      box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
    }
  }

  .optimize-btn {
    position: absolute;
    right: 8px;
    bottom: 8px;
    padding: 0.4rem 0.8rem;
    background: #13c2c2;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 0.3rem;

    &:hover:not(:disabled) {
      background: #08979c;
    }

    &:disabled {
      background: #b5f5ec;
      cursor: not-allowed;
    }

    .loading-icon {
      display: inline-block;
      width: 12px;
      height: 12px;
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      border-top-color: white;
      animation: spin 1s linear infinite;
    }
  }
}

.examples {
  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    color: #666;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 0.8rem;
  }

  li {
    padding: 0.4rem 0.8rem;
    background: #f0f0f0;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      background: #e0e0e0;
    }
  }
}

.next-btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background: #304156;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;

  &:hover:not(:disabled) {
    background: #096dd9;
  }

  &:disabled {
    background: #bae7ff;
    cursor: not-allowed;
  }
}

/* 生成中区域样式 */
.generation-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.status-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;

  .module-tag {
    padding: 0.25rem 0.5rem;
    background: #1890ff;
    color: white;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .status-message {
    flex: 1;
    font-size: 1rem;
    color: #333;

    .dots {
      span {
        opacity: 0.3;
        transition: opacity 0.3s;

        &.active {
          opacity: 1;
        }
      }
    }
  }

  .progress-text {
    font-family: monospace;
    font-size: 1rem;
    color: #666;
  }
}

.progress-container {
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  margin-bottom: 1.5rem;
  overflow: hidden;

  .progress-bar {
    height: 100%;
    background: #13c2c2;
    border-radius: 3px;
    transition: width 0.5s ease-out;
  }
}

.code-preview {
  background: #f8f8f8;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  max-height: 400px;
  overflow-y: auto;
}

.action-buttons {
  display: flex;
  justify-content: space-between;

  button {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 4px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }

  .view-btn {
    background: #304156;
    color: white;

    &:hover:not(:disabled) {
      background: #304156;
    }

    &:disabled {
      background: #bae7ff;
      cursor: not-allowed;
    }
  }

  .cancel-btn {
    background: #f0f0f0;
    color: #666;

    &:hover {
      background: #e0e0e0;
    }
  }
}

/* 结果区域样式 */
.result-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.result-header {
  margin-bottom: 1.5rem;

  h2 {
    margin: 0 0 0.5rem 0;
    color: #1890ff;
  }

  .meta-info {
    display: flex;
    gap: 1.5rem;
    font-size: 0.9rem;
    color: #666;
  }
}

.code-actions {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 1rem;

  .action-btn {
    padding: 0.5rem 1rem;
    background: #f0f0f0;
    border: none;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    transition: all 0.2s;

    &:hover {
      background: #e0e0e0;
    }

    .icon-copy, .icon-download, .icon-refresh {
      font-size: 1em;
    }
  }
}

.full-code-container {
  background: #f8f8f8;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  max-height: 500px;
  overflow-y: auto;
}

.back-btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background: #666;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;

  &:hover {
    background: #555;
  }
}

/* 通知样式 */
.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 0.8rem 1.2rem;
  border-radius: 4px;
  color: white;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

  &.info {
    background: #1890ff;
  }

  &.success {
    background: #52c41a;
  }

  &.warning {
    background: #faad14;
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

/* 动画 */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.code-history-container {
  display: flex;
  gap: 1rem;
  height: 400px;
  margin-bottom: 1.5rem;
}

.code-timeline {
  width: 200px;
  border-right: 1px solid #e8e8e8;
  overflow-y: auto;
}

.timeline-item {
  padding: 0.5rem;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.3s;

  &.active {
    border-left-color: #1890ff;
    background: #f0f9ff;
  }
}

.timeline-badge {
  width: 8px;
  height: 8px;
  background: #d9d9d9;
  border-radius: 50%;
  display: inline-block;
  margin-right: 0.5rem;
}

.timeline-content {
  display: inline-flex;
  flex-direction: column;
}

.time {
  font-size: 0.7rem;
  color: #999;
}

.module {
  font-weight: 500;
}

.code-display {
  flex: 1;
  position: relative;
}

.code-meta {
  position: absolute;
  bottom: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  border-radius: 4px 0 0 0;
}
</style>
