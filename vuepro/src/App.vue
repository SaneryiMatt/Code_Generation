<template>
  <div id="app" class="container">
    <!-- 左侧聊天窗口和消息输入框 -->
    <div class="left-pane">
      <div class="chat-box">
        <h2>Chat Window</h2>
        <div v-for="(message, index) in messages" :key="index" class="chat-message" :class="message.sender">
          <div class="message-content">
            <strong>{{ message.sender }}:</strong> {{ message.text }}
          </div>
        </div>
      </div>

      <!-- 消息发送框 -->
      <div class="message-input">
        <textarea v-model="chatMessage" placeholder="Type your message..."></textarea>
        <button @click="sendChatMessage">Send</button>
      </div>
    </div>

    <!-- 右侧表单 -->
    <div class="right-pane">
      <h2>Submit Form</h2>
      <form @submit.prevent="submitForm">
        <label for="system_name">System Name</label>
        <input type="text" id="system_name" v-model="form.system_name" required />

        <label for="save_path">Save Path</label>
        <div class="file-input-wrapper">
          <input type="text" id="save_path" v-model="form.save_path" readonly />
          <button type="button" @click="openFileDialog">Choose</button>
          <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" />
        </div>

        <label for="code_language">Code Language</label>
        <select id="code_language" v-model="form.code_language" required>
          <option value="" disabled>Select a language</option>
          <option value="Python">Python</option>
          <option value="Java">Java</option>
          <option value="C++">C++</option>
        </select>

        <label for="description">Description</label>
        <textarea id="description" v-model="form.description"></textarea>

        <div v-for="(feature, index) in form.features" :key="index">
          <label :for="'feature_' + index">Feature {{ index + 1 }} Name</label>
          <input :id="'feature_' + index" v-model="feature.feature_name" required />

          <label :for="'feature_desc_' + index">Feature {{ index + 1 }} Description</label>
          <textarea :id="'feature_desc_' + index" v-model="feature.feature_description" required></textarea>

          <button type="button" @click="removeFeature(index)">Delete</button>
        </div>

        <button type="button" @click="addFeature">Add Feature</button>
        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        system_name: '',
        save_path: '',
        code_language: '',
        description: '',
        features: [{ feature_name: '', feature_description: '' }]
      },
      chatMessage: '', // 聊天输入框中的消息
      messages: [] // 聊天和表单信息列表
    };
  },
  methods: {
    addFeature() {
      this.form.features.push({ feature_name: '', feature_description: '' });
    },
    removeFeature(index) {
      this.form.features.splice(index, 1);
    },
    openFileDialog() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        // 只能获取文件名，不能获取完整路径
        this.form.save_path = file.name;
      }
    },
    async submitForm() {
      const payload = {
        system_name: this.form.system_name,
        save_path: this.form.save_path,
        code_language: this.form.code_language,
        description: this.form.description,
        features: this.form.features
      };

      try {
        // 将表单提交信息显示在左侧聊天窗口
        this.messages.push({ sender: 'User', text: `Submitted system name: ${this.form.system_name}` });

        // 调用 Flask 后端 API
        const response = await axios.post('http://localhost:5000/api/chat', payload);

        // 显示后端返回的消息
        response.data.messages.forEach(msg => {
          this.messages.push({ sender: 'AI', text: `${msg.title}: ${msg.content}` });
        });
      } catch (error) {
        console.error('Error submitting form:', error);
      }

      // 清空表单
      this.form = {
        system_name: '',
        save_path: '',
        code_language: '',
        description: '',
        features: [{ feature_name: '', feature_description: '' }]
      };
    },
    // 用户发送聊天消息
    sendChatMessage() {
      if (this.chatMessage.trim()) {
        // 将消息添加到聊天记录中
        this.messages.push({ sender: 'User', text: this.chatMessage });
        this.chatMessage = ''; // 清空输入框
      }
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
}

.left-pane {
  width: 50%;
  padding: 20px;
  border-right: 1px solid #ccc;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
}

.right-pane {
  width: 50%;
  padding: 20px;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  background-color: #e6e6e6;
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.chat-message {
  max-width: 70%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 15px;
  word-wrap: break-word;
}

.chat-message.User {
  background-color: #d1e7dd;
  align-self: flex-end;
}

.chat-message.AI {
  background-color: #f8d7da;
  align-self: flex-start;
}

.message-input {
  display: flex;
  align-items: center;
  padding: 10px;
}

.message-input textarea {
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  margin-right: 10px;
}

.message-input button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

form {
  display: flex;
  flex-direction: column;
}

input, select, textarea, button {
  margin-bottom: 15px;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.file-input-wrapper {
  display: flex;
  align-items: center;
}

button {
  cursor: pointer;
}
</style>
