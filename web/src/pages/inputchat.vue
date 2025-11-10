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
      <!-- 豆包的深度思考样式 -->
      <div data-testid="use-smart-mode-switch-btn" class="action-item-kihiq2">
        <button 
          :data-checked="isSmartMode"
          class="semi-button"
          type="button" 
          aria-disabled="false"
          @click="isSmartMode = !isSmartMode; handleModeChange()"
          :class="{ active: isSmartMode}"
        >
          <span class="semi-button-content">
            <span role="img" class="semi-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M12 14.019a2.02 2.02 0 1 0 0-4.04 2.02 2.02 0 0 0 0 4.04"></path><path fill="currentColor" fill-rule="evenodd" d="M2.059 6.209c-.14-.932-.098-2.259.897-3.253.994-.995 2.321-1.037 3.253-.897.98.147 2.02.556 3.026 1.084.878.46 1.81 1.052 2.765 1.753a22 22 0 0 1 2.765-1.753c1.007-.527 2.046-.937 3.026-1.084.932-.14 2.259-.097 3.253.897s1.037 2.321.897 3.253c-.147.98-.557 2.02-1.084 3.026-.46.878-1.052 1.81-1.753 2.765a22 22 0 0 1 1.753 2.765c.527 1.007.937 2.046 1.084 3.026.14.932.098 2.259-.897 3.253-.994.994-2.321 1.037-3.253.897-.98-.147-2.02-.557-3.026-1.084A22 22 0 0 1 12 19.104a22 22 0 0 1-2.766 1.754c-1.006.527-2.045.936-3.025 1.083-.932.14-2.259.098-3.253-.897-.995-.994-1.037-2.321-.897-3.253.147-.98.556-2.02 1.084-3.026A22 22 0 0 1 4.896 12a22 22 0 0 1-1.753-2.766C2.616 8.228 2.206 7.19 2.059 6.21m2.325-1.825c.892-.892 3.238-.1 5.969 1.816-.724.613-1.45 1.28-2.161 1.992a36 36 0 0 0-1.992 2.16c-1.916-2.73-2.708-5.076-1.816-5.968M9.62 9.62A33 33 0 0 0 7.455 12a33 33 0 0 0 2.165 2.38A33 33 0 0 0 12 16.545a33 33 0 0 0 2.38-2.165A33 33 0 0 0 16.545 12a33 33 0 0 0-2.165-2.38A33 33 0 0 0 12 7.455 33 33 0 0 0 9.62 9.62m-5.236 9.996c-.892-.892-.1-3.238 1.816-5.969.613.724 1.28 1.449 1.992 2.16.712.713 1.437 1.38 2.161 1.993-2.73 1.916-5.077 2.708-5.97 1.816m15.232 0c-.892.892-3.238.1-5.969-1.816a36 36 0 0 0 2.16-1.992 36 36 0 0 0 1.993-2.161c1.916 2.73 2.708 5.077 1.816 5.969M15.808 8.192a36 36 0 0 1 1.992 2.16c1.915-2.73 2.708-5.076 1.816-5.968s-3.238-.1-5.969 1.816c.724.613 1.45 1.28 2.161 1.992" clip-rule="evenodd"></path></svg>
            </span>
            <span class="semi-button-content-right">
              <div style="display: flex;align-items: center;">智能模式</div>
            </span>
          </span>
        </button>
      </div>
      <!--  -->
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
  emits: ['update:modelValue', 'send','update:smartMode'],
  data() {
    return {
      localInput: this.modelValue,
      isSmartMode: false
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
    },
    handleModeChange() {
    this.$emit('update:smartMode', this.isSmartMode);
  }
  }
};
</script>

<style scoped>
.semi-button {
  padding: 8px 12px;
  background-color: #b7e4c7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
  height: 70%;
  -webkit-user-select:none;/*webkit浏览器*/ 
  -moz-user-select:none;/*火狐*/ 
  -ms-user-select:none;/*IE10*/ 
  user-select:none;
}
.semi-button:hover {
  outline: none;
  box-shadow: 0 0 0 3px rgba(183, 228, 199, 0.5);
}
.semi-button.active {
  background-color: #40c057;
  /* 找不到好看的颜色 */
  color: white;
  /* box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2); */
}
.semi-button-content {
  display: flex;
  align-items: center;
  gap: 6px;
}
.semi-button-content-right {
  margin-left: 4px;
  font-size: 16px;
}
.semi-icon {
  display: inline-block;
    font-style: normal;
    line-height: 0;
    text-align: center;
    text-rendering: optimizeLegibility;
    text-transform: none;
    fill: currentColor;
}


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