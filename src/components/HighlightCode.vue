<template>
  <pre><code ref="codeEl" :class="`language-${language}`"></code></pre>
</template>

<script>
import { ref, watch, onMounted, nextTick } from 'vue'
import hljs from 'highlight.js'

export default {
  props: {
    code: String,
    language: String,
    showLineNumbers: Boolean
  },
  setup(props) {
    const codeEl = ref(null)

    const highlightCode = async () => {
      await nextTick()
      if (codeEl.value) {
        // 安全地设置文本内容（自动转义HTML）
        codeEl.value.textContent = props.code || ''

        // 移除之前的高亮标记
        delete codeEl.value.dataset.highlighted

        // 仅当有内容时进行高亮
        if (props.code) {
          try {
            hljs.highlightElement(codeEl.value)
          } catch (error) {
            console.error('高亮失败:', error)
          }
        }
      }
    }

    onMounted(highlightCode)
    watch(() => [props.code, props.language], highlightCode)

    return { codeEl }
  }
}
</script>
