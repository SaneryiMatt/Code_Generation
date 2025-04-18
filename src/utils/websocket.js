export function createCodeGenSocket(store) {
  // 开发环境下不创建真实WebSocket
  if (import.meta.env.DEV) return null

  const socket = new WebSocket('ws://your-api-endpoint/ws/codegen')

  socket.onopen = () => {
    console.log('WebSocket连接已建立')
    socket.send(JSON.stringify({
      type: 'init',
      prompt: store.userInput
    }))
  }

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    switch(data.type) {
      case 'progress':
        store.progress = data.value
        break
      case 'module':
        store.currentModule = data.name
        break
      case 'chunk':
        store.generatedCode += data.content
        break
      case 'file':
        store.generatedFiles.push(data.file)
        break
      case 'error':
        store.showNotification(data.message, 'error')
        break
      case 'complete':
        store.isGenerating = false
        socket.close()
        store.showNotification('代码生成完成!', 'success')
        break
    }
  }

  socket.onclose = () => {
    console.log('WebSocket连接已关闭')
  }

  socket.onerror = (error) => {
    console.error('WebSocket错误:', error)
    store.showNotification('连接发生错误，请重试', 'error')
  }

  return socket
}
