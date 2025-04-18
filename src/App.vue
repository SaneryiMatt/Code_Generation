<template>
  <div class="codegen-app">
    <!-- 仅保留头部导航栏 -->
    <header class="app-header">
      <h1>AI代码生成系统</h1>
    </header>

    <!-- 主内容区直接渲染HomeView -->
    <main class="app-main">
       <router-view />
    </main>
  </div>
</template>

<script setup>


</script>

<style scoped lang="scss">
.codegen-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
}

.app-header {
  background-color: #304156;
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
  }
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}
.app-main {
  position: relative;
  z-index: 1;
}
</style>
