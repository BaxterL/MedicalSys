<!-- ChatInput.vue -->
<template>
  <div class="pre-chat-input-container">
    <div class="chatc-up">
      <textarea
        v-model="localInput"
        @keydown.enter.prevent="handleSend"
        placeholder="发送消息"
        class="pre-chat-input"
        rows="3"
        ref="inputRef"
      ></textarea>
    </div>
    <div class="chatc-down">
      <div style="flex: 1 1;"></div>
      <div class="chatc-tools">
        <div class="chatc-tools-button">
          <button
            @click="handleSend"
            class="pre-chat-send-btn"
            :disabled="!localInput.trim()"
            aria-label="发送"
            >
            <span style="display: flex;align-items: center; justify-content: center;">
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                <path fill="currentColor" d="m3.543 8.883 7.042-7.047a2 2 0 0 1 2.828 0l7.043 7.046a1 1 0 0 1 0 1.415l-.701.701a1 1 0 0 1-1.414 0L13.3 5.956v15.792a1 1 0 0 1-1 1h-.99a1 1 0 0 1-1-1V6.342l-4.654 4.656a1 1 0 0 1-1.414 0l-.7-.7a1 1 0 0 1 0-1.415"></path>
              </svg>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatInput',
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue', 'send'],
  data() {
    return {
      localInput: this.modelValue
    };
  },
  watch: {
    modelValue(newVal) {
      this.localInput = newVal;
    }
  },
  methods: {
    handleSend() {
      const text = this.localInput.trim();
      if (!text) return;
      this.$emit('send', text);
      this.localInput = '';
      this.$emit('update:modelValue', '');
    },
    focusInput() {
      this.$refs.inputRef?.focus();
    }
  }
};
</script>

<style scoped>
.pre-chat-input-container {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: #fff;
  padding: 12px;
  border-radius: 14px;
}

.chatc-up {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 12px;
}

.chatc-down {
  align-items: flex-end;
  display: flex;
  width: 100%;
  margin-top: 8px;
}

.chatc-tools {
  display: flex;
  flex-direction: row;
  gap: 8px;
}

.chatc-tools-button {
  display: flex;
  align-items: center;
}

.pre-chat-input {
  width: 96%;
  flex: 1;
  padding: 12px;
  font-size: 18px;
  border: none;
  resize: none;
  outline: none;
  box-shadow: 0 2px 8px rgba(34, 230, 93, 0.08);
}

.pre-chat-send-btn {
  padding: 12px 24px;
  background-color: #40c057;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pre-chat-send-btn:disabled {
  background-color: #b7e4c7;
  cursor: not-allowed;
}
</style>