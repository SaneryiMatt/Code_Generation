<template>
  <div>
    <input v-model="question" placeholder="输入你的问题" />
    <button @click="sendMessage">发送问题</button>
    <div v-html="response"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: null,
      question: "",
      response: ""
    };
  },
  mounted() {
    // 建立 WebSocket 连接
    this.socket = io('http://localhost:5000'); // 根据后端的地址调整
    // 监听 WebSocket 消息
    this.socket.on('chat_response', (data) => {
      this.response += data.response + "<br>";  // 逐步更新响应内容
    });
  },
  methods: {
    sendMessage() {
      // 向服务器发送问题
      this.socket.emit('chat_message', { message: this.question });
      this.response = "";  // 清空之前的回答
    }
  }
};
</script>

<style scoped>
/* 你可以在这里定义一些样式 */
</style>
