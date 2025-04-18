<template>
  <div class="result-section">
    <div class="result-header">
      <h2>代码生成完成</h2>
    </div>

    <div class="code-explorer">
      <!-- 文件树 -->
      <div class="file-tree">
        <div class="tree-header">生成的文件</div>
        <ul>
          <li v-for="file in store.generatedFiles"
              :key="file.name"
              :class="{ active: store.currentFile === file.name }"
              @click="handleFileClick(file)">
            <span class="file-icon">
              {{ fileIcon(file.type) }}
            </span>
            {{ file.name }}
          </li>
        </ul>
      </div>

      <!-- 代码展示区 -->
      <div class="code-viewer">
        <div class="file-header">
          <span class="file-name">{{ store.currentFile }}</span>
          <span v-if="store.isTyping" class="typing-dots">{{ store.typingDots }}</span>
          <div class="file-actions">
            <button @click="copyCode" class="icon-btn" title="复制">
              <i class="icon-copy"></i>
            </button>
            <button @click="downloadCurrent" class="icon-btn" title="下载">
              <i class="icon-download"></i>
            </button>
          </div>
        </div>
        <div class="code-container">
          <div v-if="store.isGenerating">⏳ 正在加载代码...</div>
          <HighlightCode
            :code="store.currentFileContent"
            :language="store.currentFileType"
            :show-line-numbers="false"
          />
        </div>
      </div>
    </div>

    <div class="global-actions">
      <button @click="downloadAll" class="action-btn">
        <i class="icon-download"></i> 同步到本地
      </button>
      <button @click="backToInput" class="action-btn">
        <i class="icon-back"></i> 返回修改
      </button>
    </div>
  </div>
      <!-- 调试信息（开发时启用） -->
    <div class="debug-info" v-if="false">
      <h4>调试信息：</h4>
      <p>当前文件: {{ store.currentFile }}</p>
      <p>文件列表: {{ store.generatedFiles.map(f => f.name).join(', ') }}</p>
      <p>内容长度: {{ store.currentFileContent?.length }}</p>
    </div>

  <!-- 全局通知 -->
  <Transition name="fade">
      <div v-if="store.notification.show" class="notification" :class="store.notification.type">
        {{ store.notification.message }}
      </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCodeGenStore } from '@/stores/codegen'
import HighlightCode from '@/components/HighlightCode.vue'
import sssssh from '@/components/Notification.vue'

const router = useRouter()
const store = useCodeGenStore()

// 文件图标映射
const fileIcon = (type) => {
  const icons = {
    entity: '📄',
    service: '📄',
    controller: '📄',
    module: '📄',
    dto: '📄',
    interface: '📄'
  }
  return icons[type] || '📄'
}

// 复制当前文件代码
const copyCode = async () => {
  await store.copyCode()
}

// 下载当前文件
const downloadCurrent = () => {
  //store.downloadCurrentFile()
  //store.showNotification('代码已同步到本地！', 'info')
}

// 下载全部文件
const downloadAll = () => {
  //store.downloadAllFiles()
  store.showNotification('代码已同步到本地！', 'info')
}

// 返回修改
const backToInput = () => {
  router.push('/')
  store.resetState()
}

// 处理文件点击
const handleFileClick = async (file) => {
  if (!file?.name) {
    console.error('无效的文件对象:', file)
    return
  }

  console.log('正在切换文件:', file.name)

  // 设置当前文件
  store.setCurrentFile(file.name)

  // 确保视图更新
  //await nextTick()
  console.log('切换后内容:', store.currentFileContent)
  document.querySelectorAll('[data-highlighted]').forEach(el => {
    delete el.dataset.highlighted
  })
}
</script>

<style scoped lang="scss">
.result-section {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 60px);
  padding: 1.5rem;
  background: white;
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

.code-explorer {
  display: flex;
  flex: 1;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
}

.file-tree {
  width: 250px;
  border-right: 1px solid #e8e8e8;
  background: #fafafa;
  overflow-x: auto;

  .tree-header {
    padding: 0.8rem;
    font-weight: bold;
    border-bottom: 1px solid #e8e8e8;
    background: #f0f0f0;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  li {
    padding: 0.6rem 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: all 0.2s;

    &:hover {
      background: #f0f0f0;
    }

    &.active {
      background: #e6f7ff;
      color: #1890ff;
    }
  }

  .file-icon {
    margin-right: 0.5rem;
  }
}

.code-viewer {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.file-header {
  padding: 0.8rem;
  background: #fafafa;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .file-name {
    font-family: monospace;
    font-weight: bold;
  }
}

.file-actions {
  display: flex;
  gap: 0.5rem;

  .icon-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.3rem;
    color: #dc18ff;

    &:hover {
      color: #1890ff;
    }
  }
}

.code-container {
  flex: 1;
  overflow-x: auto;       // ✅ 横向滚动
  overflow-y: auto;
  background: #f8f8f8;
  padding: 1rem;
  white-space: pre;        // ✅ 保证代码不换行
  max-width: 100%;         // ✅ 限制宽度
  /* 防止行号重复 */
  pre[class*="language-"] .line-numbers-rows {
    display: none;
  }
}
pre, code {
  white-space: pre;
}

.global-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;

  .action-btn {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 4px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s;

    &:hover {
      opacity: 0.9;
    }

    &.download-btn {
      background: #1890ff;
      color: white;
    }

    &.back-btn {
      background: #f0f0f0;
      color: #666;
    }
  }
  .typing-dots {
  font-family: monospace;
  margin-left: 0.5rem;
  color: #999;
  font-size: 1.2rem;
  animation: blink 1s step-start infinite;
}

@keyframes blink {
  50% {
    opacity: 0.5;
  }
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

</style>
