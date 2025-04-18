<template>
  <div id="particles-js" class="particles-container">
    <div class="content">
      <!-- 您的内容 -->
    </div>
  </div>
</template>

<script>
//import particlesJS from 'particles.js'

export default {
  name: 'ParticlesBackground',
  mounted() {
    this.initParticles()
  },
  methods: {
    initParticles() {
      particlesJS('particles-js', {
        particles: {
          number: { value: 80, density: { enable: true, value_area: 800 } },
          color: { value: "#ffffff" },
          shape: { type: "circle" },
          opacity: { value: 0.5, random: true },
          size: { value: 3, random: true },
          line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
          move: { enable: true, speed: 2, direction: "none", random: true, straight: false, out_mode: "out" }
        },
        interactivity: {
          detect_on: "canvas",
          events: {
            onhover: { enable: true, mode: "grab" },
            onclick: { enable: true, mode: "push" }
          }
        }
      })
    }
  }
}
</script>

<style>
.particles-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
}

.content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}
</style>
