import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useCodeGenStore = defineStore('codegen', () => {
  // 状态
  const userInput = ref('')
  const generatedCode = ref('')
  const progress = ref(0)
  const currentModule = ref('')
  const language = ref('typescript')
  const isOptimizing = ref(false)
  const isGenerating = ref(false)
  const generateTime = ref('')
  const notification = ref({
    show: false,
    type: 'info',
    message: ''
  })
  const codeHistory = ref([])
  const currentHistoryIndex = ref(-1)
  const generatedFiles = ref([])
  const currentFile = ref('')
  let socket = null

  // 计算属性
  const generationStatus = computed(() => {
    if (progress.value < 20) return '分析需求中'
    if (progress.value < 70) return '构建数据结构'
    return '生成业务逻辑'
  })

  const currentHistory = computed(() =>
    codeHistory.value[currentHistoryIndex.value] || {}
  )

  const currentCode = computed(() =>
    currentHistory.value.code || generatedCode.value
  )

  const currentFileContent = computed(() => {
    if (!currentFile.value) return '// 请选择文件'
    const foundFile = generatedFiles.value.find(f => f.name === currentFile.value)
    return foundFile?.content || '// 文件内容为空'
  })

  const currentFileType = computed(() => {
    return currentFile.value.split('.').pop() || 'typescript'
  })

  // 方法
  const setUserInput = (input) => {
    userInput.value = input
  }

  const setCurrentHistoryIndex = (index) => {
    currentHistoryIndex.value = index
  }

  const setCurrentFile = (filename) => {
    currentFile.value = filename
  }

  const showNotification = (message, type = 'info') => {
    notification.value = { show: true, message, type }
    setTimeout(() => {
      notification.value.show = false
    }, 3000)
  }

  const optimizeText = async () => {
    if (!userInput.value.trim()) return

    isOptimizing.value = true
    try {
      const response = await axios.post('/stream', {
        text: userInput.value
      })

      if (response.data?.optimizedText) {
        userInput.value = response.data.optimizedText
        showNotification('需求描述已优化', 'success')
      }
    } catch (error) {
      console.error('优化失败:', error)
      showNotification('优化失败: ' + (error.response?.data?.message || '服务异常'), 'error')
    } finally {
      isOptimizing.value = false
    }
  }

  const startGeneration = async () => {
    if (!userInput.value.trim()) return

    progress.value = 0
    generatedCode.value = ''
    currentModule.value = '分析需求'
    isGenerating.value = true
    generateTime.value = new Date().toLocaleString()
    codeHistory.value = []
    generatedFiles.value = []

    // 创建 WebSocket 连接
    socket = new WebSocket('ws://127.0.0.1:8000/dify/stream');  // 使用你的 WebSocket API 地址

    socket.onopen = () => {
      console.log('WebSocket 连接已建立');
      socket.send(JSON.stringify({ query: userInput.value })); // 发送请求数据到后端
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.code) {
        generatedCode.value += data.code;  // 拼接生成的代码
      }

      // 如果生成完成，关闭 WebSocket 连接
      if (data.progress >= 100) {
        isGenerating.value = false;
        socket.close();
        showNotification('代码生成完成!', 'success');
      }
    };

    socket.onerror = (error) => {
      console.error('WebSocket 错误:', error);
      showNotification('WebSocket连接失败', 'error');
      isGenerating.value = false;
    };

    socket.onclose = () => {
      console.log('WebSocket 连接已关闭');
    };
  }

  const cancelGeneration = () => {
    if (socket) {
      socket.close();  // 关闭 WebSocket 连接
    }
    isGenerating.value = false
    generatedCode.value = ''
    showNotification('已取消生成', 'warning')
  }

  const copyCode = async () => {
    try {
      const textToCopy = currentFile.value
        ? currentFileContent.value
        : generatedCode.value

      await navigator.clipboard.writeText(textToCopy)
      showNotification('代码已复制到剪贴板', 'success')
      return true
    } catch (err) {
      console.error('复制失败:', err)
      showNotification('复制失败，请手动选择代码', 'error')
      return false
    }
  }

  const downloadCurrentFile = () => {
    const content = currentFileContent.value
    const filename = currentFile.value || `generated-${Date.now()}.${currentFileType.value}`
    downloadFile(content, filename)
    showNotification('文件已下载', 'success')
  }

  const downloadAllFiles = () => {
    // 实际项目中可以实现ZIP打包下载
    generatedFiles.value.forEach(file => {
      downloadFile(file.content, file.name)
    })
    showNotification('开始下载全部文件', 'info')
  }

  const downloadFile = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const resetState = () => {
    userInput.value = ''
    generatedCode.value = ''
    progress.value = 0
    currentModule.value = ''
    isGenerating.value = false
    isOptimizing.value = false
    codeHistory.value = []
    generatedFiles.value = []
    currentFile.value = ''
  }

  const initState = () => {
    if (import.meta.env.DEV) {
      userInput.value = '创建学生管理系统，包含姓名、学号、班级字段'
    }
  }

  return {
    // 状态
    userInput,
    generatedCode,
    progress,
    currentModule,
    language,
    isOptimizing,
    isGenerating,
    generateTime,
    notification,
    codeHistory,
    currentHistoryIndex,
    generatedFiles,
    currentFile,

    // 计算属性
    generationStatus,
    currentHistory,
    currentCode,
    currentFileContent,
    currentFileType,

    // 方法
    setUserInput,
    setCurrentHistoryIndex,
    setCurrentStep,
    setCurrentFile,
    showNotification,
    optimizeText,
    startGeneration,
    cancelGeneration,
    copyCode,
    downloadCurrentFile,
    downloadAllFiles,
    resetState,
    initState
  }
})
