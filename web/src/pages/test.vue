<template>
  <div class="chat-container">
    <!-- 初始状态：仅居中的聊天框 -->
    <div v-if="messages.length === 0" class="initial-state">
      <div class="initial-input-container">
        <textarea
          v-model="newMessage"
          @keydown.enter.prevent="sendMessage"
          placeholder="输入消息开始对话..."
          class="initial-message-input"
          rows="3"
          ref="initialInput"
        ></textarea>
        <button 
          @click="sendMessage"
          class="initial-send-btn"
          :disabled="!newMessage.trim()"
        >
          发送
        </button>
      </div>
    </div>

    <!-- 有消息后的状态 -->
    <div v-else class="conversation-state">
      <!-- 聊天记录区域 -->
      <div class="chat-messages" ref="chatContainer">
        <div class="messages-container">
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            class="message-item"
            :class="{ 
              'user-message': message.isUser, 
              'ai-message': !message.isUser
            }"
          >
            <!-- 消息气泡 -->
            <div class="message-bubble" :class="{ 'user-bubble': message.isUser, 'ai-bubble': !message.isUser }">
              <p class="message-text">{{ message.text }}</p>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部输入区域 -->
      <div class="bottom-input-area">
        <textarea
          v-model="newMessage"
          @keydown.enter.prevent="sendMessage"
          placeholder="输入消息..."
          class="bottom-message-input"
          rows="3"
          ref="bottomInput"
        ></textarea>
        <button 
          @click="sendMessage"
          class="bottom-send-btn"
          :disabled="!newMessage.trim()"
        >
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      newMessage: ''
    };
  },
  methods: {
    sendMessage() {
      const message = this.newMessage.trim();
      if (!message) return;

      // 添加用户消息
      this.messages.push({
        text: message,
        isUser: true,
        timestamp: new Date()
      });

      // 清空输入框
      this.newMessage = '';

      // 自动聚焦到底部输入框（如果是首次发送）
      if (this.messages.length === 1) {
        this.$nextTick(() => {
          this.$refs.bottomInput.focus();
        });
      }

      // 模拟AI回复
      setTimeout(() => {
        const aiReply = `这是对"${message}"的回复。你可以根据实际需求替换为真实的AI响应。`;
        this.messages.push({
          text: aiReply,
          isUser: false,
          timestamp: new Date()
        });
        
        // 滚动到底部
        this.scrollToBottom();
      }, 800);

      // 滚动到底部
      this.scrollToBottom();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContainer = this.$refs.chatContainer;
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      });
    },
    formatTime(timestamp) {
      return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  },
  mounted() {
    // 初始聚焦到居中的输入框
    this.$nextTick(() => {
      this.$refs.initialInput?.focus();
    });
  }
};
</script>

<style scoped>
.chat-container {
  width: 100%;
  height: 100vh;
  background-color: #f9fafb;
  overflow: hidden;
}

/* 初始状态样式 - 仅居中的聊天框 */
.initial-state {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

.initial-input-container {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: fadeIn 0.5s ease-out;
}

.initial-message-input {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  font-size: 16px;
  resize: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.initial-message-input:focus {
  outline: none;
  border-color: #93c5fd;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
}

.initial-send-btn {
  align-self: flex-end;
  padding: 10px 20px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.initial-send-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.initial-send-btn:not(:disabled):hover {
  background-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.15);
}

/* 对话状态样式 - 有消息记录时 */
.conversation-state {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
  animation: slideUp 0.3s ease-out;
}

.messages-container {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
  animation: fadeIn 0.3s ease-out;
}

.ai-message {
  justify-content: flex-start;
}

.user-message {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.ai-bubble {
  background-color: white;
  color: #1f2937;
  border: 1px solid #e5e7eb;
}

.user-bubble {
  background-color: #3b82f6;
  color: white;
}

.message-text {
  line-height: 1.5;
  margin-bottom: 4px;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  text-align: right;
}

/* 底部输入区域 */
.bottom-input-area {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #e5e7eb;
  background-color: white;
  box-sizing: border-box;
  animation: slideUp 0.3s ease-out;
}

.bottom-message-input {
  flex: 1;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 16px;
  resize: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.bottom-message-input:focus {
  outline: none;
  border-color: #93c5fd;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.bottom-send-btn {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  align-self: flex-end;
}

.bottom-send-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.bottom-send-btn:not(:disabled):hover {
  background-color: #2563eb;
}

/* 动画 */
@keyframes fadeIn {
  from { 
    opacity: 0;
  }
  to { 
    opacity: 1;
  }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: #c1c1c1;
  border-radius: 3px;
}

/* 响应式调整 */
@media (max-width: 640px) {
  .message-bubble {
    max-width: 75%;
  }
}
</style>
