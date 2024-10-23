<template>
  <div class="requirement-form">
    <h2>软件系统开发需求表单</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="projectName">项目名称:</label>
        <input type="text" v-model="form.projectName" required />
      </div>
      <div>
        <label for="features">功能需求:</label>
        <textarea v-model="form.features" required></textarea>
      </div>
      <div>
        <label for="targetUsers">目标用户:</label>
        <input type="text" v-model="form.targetUsers" required />
      </div>
      <div>
        <label for="priority">优先级:</label>
        <select v-model="form.priority" required>
          <option value="" disabled>请选择</option>
          <option value="高">高</option>
          <option value="中">中</option>
          <option value="低">低</option>
        </select>
      </div>
      <div>
        <label for="deadline">预计完成时间:</label>
        <input type="date" v-model="form.deadline" required />
      </div>
      <button type="submit">提交需求</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        projectName: '',
        features: '',
        targetUsers: '',
        priority: '',
        deadline: ''
      }
    };
  },
  methods: {
    submitForm() {
      // 提交表单数据，可以通过 Axios 发送到后端
      console.log('表单提交:', this.form);
      // 发送到后端逻辑
      axios.post('http://localhost:5000/api/requirements', this.form)
         .then(response => {
           console.log('响应:', response.data);
        })
         .catch(error => {
           console.error('提交失败:', error);
       });
    }
  }
}
</script>

<style scoped>
.requirement-form {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.requirement-form div {
  margin-bottom: 15px;
}
</style>
