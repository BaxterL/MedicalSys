<template>
  <div class="chat-page">
    <Nvabar />
    <transition name="fade-slide" mode="out-in">
      <div v-if="messages.length === 0" class="pre-chat" key="pre">
        <div class="pre-chat-msg">
          <h2 class="pre-chat-msg-h2" ref="typeitElement"></h2>
        </div>
        <inputchat v-model="input" @send="handleSend" ref="chatInputRef" />
      </div>
      <div v-else class="chat-container" key="chat">
        <div v-if="messages.length" class="chat-history">
          <div v-for="(msg, idx) in messages" :key="idx" :class="msg.role === 'user' ? 'bubble user' : 'bubble ai'">
            <span v-if="msg.role === 'ai'" class="bubble-label">医疗助手：</span>
            <span v-if="msg.role === 'ai' && typing && idx === messages.length - 1" v-html="typingText"></span>
            <span v-else v-html="msg.text"></span>
          </div>
        </div>
        <inputchat v-model="input" @send="handleSend" ref="chatInputRef" />
        <!-- <div class="pre-chat-input-container">
          <div class="chatc-up">
            <textarea v-model="input" @keydown.enter.prevent="handleSend" placeholder="发送消息" class="pre-chat-input"
              rows="3" ref="initialInput"></textarea>
          </div>
          <div class="chatc-down">
            <div style="flex: 1 1;"></div>
            <div class="chatc-tools">
              <div class="chatc-tools-button">
                <button @click="handleSend" class="pre-chat-send-btn" :disabled="!input.trim()" aria-label="">
                  <span style="display: flex;align-items: center; justify-content: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                      <path fill="currentColor"
                        d="m3.543 8.883 7.042-7.047a2 2 0 0 1 2.828 0l7.043 7.046a1 1 0 0 1 0 1.415l-.701.701a1 1 0 0 1-1.414 0L13.3 5.956v15.792a1 1 0 0 1-1 1h-.99a1 1 0 0 1-1-1V6.342l-4.654 4.656a1 1 0 0 1-1.414 0l-.7-.7a1 1 0 0 1 0-1.415">
                      </path>
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>
          </div> -->
      </div>
      <!-- <div v-else class="chat-container" key="chat">
        <div v-if="messages.length" class="chat-history">
          <div v-for="(msg, idx) in messages" :key="idx" :class="msg.role === 'user' ? 'bubble user' : 'bubble ai'">
            <span v-if="msg.role === 'ai'" class="bubble-label">医疗助手：</span>
            <span v-if="msg.role === 'ai' && typing && idx === messages.length - 1" v-html="typingText"></span>
            <span v-else v-html="msg.text"></span>
          </div>
        </div>
        <div class="chat-input-bar">
          <div class="chatc-up">
            <input v-model="input" type="text" placeholder="请输入你的问题..." @keyup.enter="handleSend" class="chat-input" />
          </div>
          <div class="chatc-down">
            <div style="flex: 1 1;"></div>
            <div class="chatc-tools">
              <div class="chatc-tools-button">
                <button class="send-btn" @click="handleSend" :disabled="!input.trim()">
                  <span style="display: flex;align-items: center; justify-content: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                      <path fill="currentColor"
                        d="m3.543 8.883 7.042-7.047a2 2 0 0 1 2.828 0l7.043 7.046a1 1 0 0 1 0 1.415l-.701.701a1 1 0 0 1-1.414 0L13.3 5.956v15.792a1 1 0 0 1-1 1h-.99a1 1 0 0 1-1-1V6.342l-4.654 4.656a1 1 0 0 1-1.414 0l-.7-.7a1 1 0 0 1 0-1.415">
                      </path>
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div> -->
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import Nvabar from './nvabar.vue';
import { ref, onMounted } from 'vue';
import TypeIt from 'typeit';
import inputchat from './inputchat.vue';

const typeitElement = ref(null);

export default {
  name: 'chat',
  components: { Nvabar, inputchat },
  data() {
    return {
      input: '',
      messages: [],
      typing: false,
      typingText: '',
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.addLinkInterception();
      this.$refs.chatInputRef?.focusInput();
      new TypeIt(this.$refs.typeitElement, {
        strings: [this.getTime()],
        speed: 80,
        loop: false,
        breakLines: false,
        cursor: false
      }).go();
    });
  },
  updated() {
    this.addLinkInterception();
  },
  methods: {
    getTime() {
      let time = new Date()
      let hours = time.getHours()
      let state = ''
      if (hours >= 0 && hours <= 11) {
        state = `上午好`
      } else if (hours > 11 && hours <= 13) {
        state = `中午好`
      } else if (hours > 13 && hours <= 18) {
        state = `下午好`
      } else if (hours > 18 && hours <= 24) {
        state = `晚上好`
      }

      var titleText = `👨‍⚕️${state}，有什么我可以帮助你的吗？`
      return titleText
    },
    addLinkInterception() {
      // 只拦截 .vue-link-btn 链接
      const container = this.$el.querySelector('.chat-history');
      if (!container) return;
      const links = container.querySelectorAll('.vue-link-btn');
      links.forEach(link => {
        link.onclick = (e) => {
          e.preventDefault();
          const href = link.getAttribute('href');
          if (href) {
            this.$router.push(href);
          }
        };
      });
    },
    async sendDeepseekMsg(text) {
      try {
        const messages = [
          { role: "system", content: "你是人工智能助手" },
          { role: "user", content: text }
        ];

        const res = await axios.post('/api/deepseek', { messages });

        const aiResponse = res.data.success ? res.data.response : 'AI 响应异常';
        await this.typeAiText(aiResponse);

        this.typing = false;
        this.$nextTick(() => {
          const history = this.$el.querySelector('.chat-history');
          if (history) history.scrollTop = history.scrollHeight;
        });
      } catch (e) {
        this.messages.push({ role: 'bug', text: `错误：${e.message || '请求失败，请稍后重试'}` });
        this.typing = false;
      }
    },
    async handleSend(text) {
      this.isDeepseek = this.$refs.chatInputRef.isDeepseek;
      text = text?.trim() || '';
      if (!text) return;
      this.messages.push({ role: 'user', text });
      this.input = '';
      this.typing = true;
      this.typingText = '';
      if (this.isDeepseek) {
        await this.sendDeepseekMsg(text)
        return
      }
      try {
        const res = await axios.post('/api/ask', null, {
          params: { msg: text }
        });
        await this.typeAiText(res.data.res);
        this.typing = false;
        this.$nextTick(() => {
          const history = this.$el.querySelector('.chat-history');
          if (history) history.scrollTop = history.scrollHeight;
        });
      } catch (e) {
        this.messages.push({ role: 'ai', text: '网络错误，请稍后重试。' });
        this.typing = false;
      }
    },
    async typeAiText(text) {
      this.typingText = '';
      for (let i = 0; i < text.length; i++) {
        this.typingText += text[i];
        await new Promise(r => setTimeout(r, 18));
      }
      this.messages.push({ role: 'ai', text: this.typingText });
      this.typingText = '';
    }
  }
};
</script>

<style scoped>
.pre-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 60px);
  background: linear-gradient(180deg, #ecf9ee 0%, #d4f0d9 100%);
  padding: 20px;
}

.pre-chat-msg-h2 {
  font-size: 32px;
}

.pre-chat-input-container {
  margin-top: 20px;
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: #fff;
  padding: 12px;
  border-radius: 14px;
}

.chatc-down {
  align-items: flex-end;
  display: flex;
}

.pre-chat-input {
  width: 96%;
  flex: 1;
  padding: 12px;
  font-size: 18px;
  /* border: 2px solid #40c057; */
  /* border-radius: 8px; */
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

.chat-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #ecf9ee 0%, #d4f0d9 100%);
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding-top: 80px;
  padding-bottom: 20px;
}

.chat-history {
  width: 100%;
  max-width: 700px;
  flex: 1;
  overflow-y: auto;
  padding: 32px 0 120px 0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.bubble {
  max-width: 80%;
  padding: 18px 24px;
  border-radius: 18px;
  font-size: 18px;
  line-height: 1.6;
  word-break: break-word;
  box-shadow: 0 2px 8px rgba(34, 230, 93, 0.08);
  position: relative;
  margin-left: 16px;
  margin-right: 16px;
}

.bubble.user {
  background: #40c057;
  color: #fff;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.bubble.ai {
  background: #fff;
  color: #1e293b;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  border: 1.5px solid #40c057;
}

.bubble-label {
  font-size: 14px;
  font-weight: 700;
  margin-right: 8px;
  color: #22c55e;
}

.chat-input-bar {
  max-width: 800px;
  box-shadow: 0 -2px 8px rgba(34, 230, 93, 0.08);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 18px 0;
  z-index: 100;
  background-color: #fff;

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

.send-btn {
  padding: 12px 24px;
  background-color: #40c057;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:disabled {
  background-color: #b7e4c7;
  cursor: not-allowed;
}

.chat-input {
  width: 480px;
  padding: 14px 18px;
  border-radius: 12px;
  border: 2px solid #40c057;
  font-size: 18px;
  margin-right: 16px;
  background: #fff;
  color: #1e293b;
  outline: none;
  transition: border 0.2s;
}

.chat-input:focus {
  border: 2px solid #22c55e;
}

.send-btn {
  padding: 14px 32px;
  border: none;
  border-radius: 12px;
  background-color: #40c057;
  color: #fff;
  font-weight: 700;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
}

.send-btn:hover {
  background-color: #22c55e;
}

.vue-link-btn {
  display: inline-block;
  background: #40c057;
  color: #fff !important;
  border-radius: 8px;
  padding: 6px 18px;
  margin: 0 4px;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.2s;
  border: none;
  cursor: pointer;
}

.vue-link-btn:hover {
  background: #22c55e;
  color: #fff !important;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(40px);
}

.fade-slide-leave-from,
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>