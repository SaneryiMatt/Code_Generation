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
  const dot1 = ref(false)
  const dot2 = ref(false)
  const dot3 = ref(false)
  const notification = ref({
    show: false,
    type: 'info',
    message: ''
  })
  const codeHistory = ref([])
  const currentHistoryIndex = ref(-1)
  const generatedFiles = ref([])
  const currentFile = ref('')
  const isTyping = ref(false)
  const typingDots = ref('')


  // 计算属性
  const generationStatus = computed(() => {
    if (progress.value < 20) return '分析需求中'
    if (progress.value < 70) return '思考数据库结构'
    return '思考完成'
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
  let fullOptimizedText = '' // 用于累积所有优化内容

  try {
    const response = await fetch('http://localhost:8000/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: userInput.value })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      console.log(`Buffer after decoding: ${buffer}`)

      // 处理所有完整的行
      const lines = buffer.split('\n')
      buffer = lines.pop() //
      console.log('收到数据块:', buffer)

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.substring(6).trim()
          console.log(`Received data: ${data}`)  // 查看每次接收到的数据

          if (data === '[DONE]') {
            // 最终更新用户输入
            userInput.value = fullOptimizedText
            return
          }

          // 累积所有优化内容
          fullOptimizedText += data

          // 可选：实时更新预览
          generatedCode.value = fullOptimizedText
        }
      }
    }
  } catch (error) {
    console.error('优化失败:', error)
    showNotification('优化失败: ' + error.message, 'error')
  } finally {
    isOptimizing.value = false
  }
}
  const startGeneration = async () => {
  if (!userInput.value.trim()) return

  isGenerating.value = true
  progress.value = 0
  generatedCode.value = ''
  generateTime.value = new Date().toLocaleString()
  console.log(userInput.value)
  try {
    await  streamGeneration(userInput.value, 'dify/stream')
    console.log("[DEBUG] 模型思考完毕")

    const tableRes = await fetch('http://localhost:8000/tables', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: userInput.value })
    })

    if (!tableRes.ok) throw new Error('表结构生成失败')
    const tableResult = await tableRes.json()
    console.log('表结构 JSON:', tableResult)

    //await loadFlaskFilesByPath()
    console.log("[DEBUG] 文件加载完毕")
    // 模拟生成进度（实际应由后端事件驱动）
    const interval = setInterval(() => {
      progress.value += 10
      if (progress.value >= 100) {
        clearInterval(interval)
        isGenerating.value = false
        showNotification('思考完成!', 'success')
      }
    }, 500)
  } catch (error) {
    isGenerating.value = false
    showNotification('生成失败: ' + error.message, 'error')
  }
}

  const simulateGeneration = () => {
    const demoStages = [
      {
        module: '实体层',
        progress: 30,
        code: `@Entity()
class Student {
  @PrimaryGeneratedColumn()
  id: number

  @Column()
  name: string
}`
      },
      {
        module: '服务层',
        progress: 60,
        code: `@Injectable()
export class StudentService {
  constructor(
    @InjectRepository(Student)
    private studentRepository: Repository<Student>
  ) {}

  async create(student: CreateStudentDto) {
    return this.studentRepository.save(student)
  }
}`
      },
      {
        module: '控制器层',
        progress: 100,
        code: `@Controller('students')
export class StudentController {
  constructor(private studentService: StudentService) {}

  @Post()
  create(@Body() dto: CreateStudentDto) {
    return this.studentService.create(dto)
  }
}`
      }
    ]

    demoStages.forEach((stage, index) => {
      setTimeout(() => {
        progress.value = stage.progress
        currentModule.value = stage.module
        generatedCode.value = stage.code

        codeHistory.value.push({
          ...stage,
          time: new Date().toLocaleTimeString()
        })
        currentHistoryIndex.value = index

        if (index === demoStages.length - 1) {
          generatedFiles.value = [
            {
              name: 'student.entity.ts',
              type: 'entity',
              content: demoStages[0].code
            },
            {
              name: 'student.service.ts',
              type: 'service',
              content: demoStages[1].code
            },
            {
              name: 'student.controller.ts',
              type: 'controller',
              content: demoStages[2].code
            }
          ]
          currentFile.value = 'student.entity.ts'
          isGenerating.value = false
          showNotification('代码生成完成!', 'success')
        }
      }, index * 2000)
    })
  }

  const realGeneration = async () => {
    try {
      const response = await axios.post('/api/generate', {
        prompt: userInput.value
      }, {
        timeout: 30000
      })

      const socket = new WebSocket(`ws://your-api/ws/generate?token=${response.data.token}`)

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data)

        progress.value = data.progress
        currentModule.value = data.module
        generatedCode.value = data.code

        codeHistory.value.push({
          module: data.module,
          progress: data.progress,
          code: data.code,
          time: new Date().toLocaleTimeString()
        })

        if (data.progress >= 100) {
          generatedFiles.value = data.files.map(file => ({
            name: file.filename,
            type: file.type,
            content: file.content
          }))
          currentFile.value = generatedFiles.value[0]?.name || ''
          isGenerating.value = false
          socket.close()
          showNotification('代码生成完成!', 'success')
        }
      }

      socket.onerror = (error) => {
        console.error('WebSocket错误:', error)
        showNotification('生成连接异常', 'error')
        resetState()
      }
    } catch (error) {
      console.error('生成失败:', error)
      showNotification('生成失败: ' + error.message, 'error')
      resetState()
    }
  }

  const cancelGeneration = () => {
    isGenerating.value = false
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
    currentStep.value = 1
  }

  const initState = () => {
    if (import.meta.env.DEV) {
      userInput.value = '创建学生管理系统，包含姓名、学号、班级字段'
    }
  }

  let currentStep = ref(1) // 新增 currentStep，用来跟踪当前步骤

  // 方法
  const setCurrentStep = (step) => { // 新增方法用来更新 currentStep
    currentStep.value = step
  }

 // 方法
  const setCurrentFileContent = (content) => {
    currentFileContent.value = content  // 更新文件内容
  }

  // 在您的codegen store中修改streamGeneration方法
const streamGeneration = async (query, endpoint) => {
  try {
    const response = await fetch(`http://localhost:8000/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      // 处理SSE消息
      const lines = buffer.split('\n')
      buffer = lines.pop() // 保留不完整的行

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.substring(6).trim()
          if (data === '[DONE]') {
            return
          }

          // 修改这里：追加内容而不是替换
          if (endpoint === 'stream') {
            // 对于语言优化，替换内容
            userInput.value = data
          } else {
            // 对于代码生成，追加内容
            generatedCode.value += data
          }
        }
      }
    }
  } catch (error) {
    console.error('Stream error:', error)
    showNotification('请求失败: ' + error.message, 'error')
  }
}

const loadFilesFromStream = async (endpoint = 'stream/code') => {
  resetState() // 可选：清空旧的生成状态
  isGenerating.value = true
  progress.value = 0
  generateTime.value = new Date().toLocaleString()

  try {
    const response = await fetch(`http://localhost:8000/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: userInput.value })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop()

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.substring(6).trim()

          if (data === '[DONE]') {
            isGenerating.value = false
            showNotification('代码生成完成!', 'success')
            return
          }

          try {
            const file = JSON.parse(data)
            if (file.name && file.content) {
             generatedFiles.value.push({
                name: file.name,
                type: file.type || 'unknown',
                content: ''
             })

              if (!currentFile.value) {
                currentFile.value = file.name
              }

              await animateFileTyping(file)

              // 模拟进度提升
              progress.value = Math.min(100, progress.value + 20)
            }
          } catch (err) {
            console.warn('非文件数据或解析失败:', err)
          }
        }
      }
    }
  } catch (error) {
    console.error('加载失败:', error)
    showNotification('请求失败: ' + error.message, 'error')
    isGenerating.value = false
  }
}

 const animateFileTyping = async (file, speed = 0.1) => {
  const target = generatedFiles.value.find(f => f.name === file.name)
  if (!target) return

  target.content = ''
   isTyping.value = true
  startTypingDots()
  for (let i = 0; i < file.content.length; i++) {
    target.content += file.content[i]
    await new Promise(resolve => setTimeout(resolve, speed))
  }

  stopTypingDots()
  isTyping.value = false
}
  let dotTimer = null

const startTypingDots = () => {
  let dots = ''
  dotTimer = setInterval(() => {
    dots = dots.length >= 3 ? '' : dots + '.'
    typingDots.value = dots
  }, 500)
}

const stopTypingDots = () => {
  clearInterval(dotTimer)
  typingDots.value = ''
}

const loadFlaskFilesByPath = async (paths) => {
  const tempInput = userInput.value
  userInput.value = tempInput
  isGenerating.value = true

  try {
    const response = await fetch("http://localhost:8000/stream/files", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paths })
    })

    const reader = response.body.getReader()
    console.log(reader)
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop()

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.substring(6).trim()
          if (data === '[DONE]') {
            showNotification('代码生成完成!', 'success')
            isGenerating.value = false
            return
          }

          try {
            const file = JSON.parse(data)
            const exists = generatedFiles.value.find(f => f.name === file.name)
            if (!exists) {
              generatedFiles.value.push({ ...file, content: '' })
              currentFile.value ||= file.name
              await animateFileTyping(file)
            }
          } catch (err) {
            // 流式字符未组成完整 JSON，可跳过
          }
        }
      }
    }
  } catch (err) {
    showNotification('加载失败: ' + err.message, 'error')
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
    dot1,
    dot2,
    dot3,
    notification,
    codeHistory,
    currentHistoryIndex,
    generatedFiles,
    currentFile,
    currentStep,
    isTyping,
    typingDots,

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
    initState,
    setCurrentFileContent,
    streamGeneration,
    loadFilesFromStream,
    startTypingDots,
    stopTypingDots,
    animateFileTyping,
    loadFlaskFilesByPath
  }
})
