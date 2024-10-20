<template>
  <div class="chat-display">
    <div v-for="(message, index) in messages" :key="index" class="chat-message">
      <div :class="message.sender">
        <strong>{{ message.sender === 'user' ? 'You' : 'GPT' }}:</strong> {{ message.text }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messages: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.chat-display {
  height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 20px;
}
.chat-message {
  margin-bottom: 10px;
}
.user {
  text-align: right;
  color: blue;
}
.gpt {
  text-align: left;
  color: green;
}
</style>
