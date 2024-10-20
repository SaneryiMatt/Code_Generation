<template>
  <div class="chat-input">
    <input v-model="input" @keydown.enter="sendMessage" placeholder="Type your message..." />
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      input: ''
    }
  },
  methods: {
    sendMessage() {
      if (this.input.trim()) {
        this.$emit('send-message', this.input); // 将消息发送到父组件
        this.input = ''; // 清空输入框
      }
    }
  }
}
</script>

<style scoped>
.chat-input {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
input {
  flex: 1;
  padding: 8px;
  font-size: 16px;
}
button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
