<template>
  <div id="app">
    <h1>GPT-like Chat Application</h1>
    <Chat />
    <ChatDisplay :messages="messages" />
    <ChatInput @send-message="handleSendMessage" />
  </div>
</template>

<script>
import Chat from './components/Chat.vue';
import ChatDisplay from './components/ChatDisplay.vue';
import ChatInput from './components/ChatInput.vue';
import axios from 'axios';  // 引入 axios

export default {
  name: 'App',
  components: {
    Chat,
    ChatDisplay,
    ChatInput
  },
  data() {
    return {
      messages: []  // 保存用户和 AI 的消息
    };
  },
  methods: {
    async handleSendMessage(message) {
      // 显示用户的消息
      this.messages.push({ sender: 'user', text: message });

      try {
        // 通过 Axios 向 Flask 后端发送 POST 请求
        const response = await axios.post('http://localhost:5000/api/chat', {
          message: message
        });

        // 获取后端返回的 AI 响应
        const aiResponse = response.data.response;

        // 将 AI 的回复添加到消息列表
        this.messages.push({ sender: 'gpt', text: aiResponse });

      } catch (error) {
        console.error("Error sending message to the server:", error);
        this.messages.push({ sender: 'gpt', text: 'Error: Could not reach the server.' });
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
