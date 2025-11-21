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
          <div v-for="msg in messages" :key="msg.id" :class="getBubbleClass(msg.role)">
            <template v-if="msg.role === 'user'">
              <span v-html="msg.text"></span>
            </template>
            <template v-else-if="msg.role === 'ai'">
              <span class="bubble-label">医疗助手：</span>
              <span v-if="msg.renderMode === 'html'" v-html="typing && isLastMsg(msg) ? typingText : msg.text"></span>

              <MarkdownRender v-else-if="msg.renderMode === 'markdown'"
                :content="typing && isLastMsg(msg) ? typingText : msg.text" />
              <!-- <component 
                :is="isSmartMode ? 'MarkdownRender' : 'span'"
                v-bind="isSmartMode 
                  ? { content: typing && idx === messages.length - 1 ? typingText : msg.text} 
                  : { vHtml: typing && idx === messages.length - 1 ? typingText : msg.text}"
                v-html="isSmartMode
                  ? { content: typing && idx === messages.length - 1 ? typingText : msg.text}
                  : { vHtml: typing && idx === messages.length - 1 ? typingText : msg.text}"
                :content="!isSmartMode ? (typing && idx === messages.length - 1 ? typingText : msg.text) : undefined"
              /> -->
            </template>
            <template v-else-if="msg.role === 'loading'">
              <div class="loading">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
              </div>
            </template>
            <template v-else-if="msg.role === 'bug'">
              <span class="bubble-label">报错信息：</span>
              <span v-html="msg.text" style="color: #ff4d4f;"></span>
            </template>
          </div>
        </div>
        <inputchat v-model="input" @send="handleSend" ref="chatInputRef" />
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import Nvabar from './nvabar.vue';
import { ref, onMounted, render } from 'vue';
import TypeIt from 'typeit';
import inputchat from './inputchat.vue';
import MarkdownRender from 'vue-renderer-markdown';

const typeitElement = ref(null);

export default {
  name: 'chat',
  components: { Nvabar, inputchat, MarkdownRender },
  computed: {
    getBubbleClass() {
      return (role) => {
        if (role === 'user') return 'bubble user';
        if (role === 'loading') return 'bubble ai loading-bubble';
        return 'bubble ai';
      };
    }
  },
  data() {
    return {
      input: '',
      messages: [],
      typing: false,
      typingText: '',
      isSmartMode: false,
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
    isLastMsg(msg) {
      return this.messages[this.messages.length - 1] === msg && this.typing;
    },
    clearLoadingMessages() {
      this.messages = this.messages.filter(msg => msg.role !== 'loading');
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
    isHtml(text) {
      return /<[^>]+>/.test(text);
    },
    pushMsg(role, text, render) {
      const msg = { role, text, id: Date.now() + Math.random() };
      if (render && role !== 'loading') {
        msg.renderMode = render;
      }
      this.messages.push(msg);
    },
    async sendDeepseekMsg(text) {
      const loadingMsgId = this.messages.length;
      // this.messages.push({ role: 'loading', text: '' })
      // const render = this.isSmartMode ? 'markdown' : 'html'
      this.pushMsg('loading', '', 'markdown')
      try {
        const res = await axios.post('/api/deepseek', {
          message: text
        })

        this.messages.splice(loadingMsgId, 1)
        if (res.data.success) {
          await this.typeAiText(res.data.response, 'markdown')
        } else {
          console.log(`msg:${res.data.message}`)
        }

        this.typing = false;
        this.$nextTick(() => {
          const history = this.$el.querySelector('.chat-history');
          if (history) history.scrollTop = history.scrollHeight;
        });
      } catch (e) {
        this.clearLoadingMessages()
        // this.messages.push({ role: 'ai', text: `错误：${e.message || '请求失败，请稍后重试'}` ,render: 'html'});
        this.pushMsg('ai', `错误：${e.message || '请求失败，请稍后重试'}`, 'html')
        this.typing = false;
      }
    },
    async handleSend(text) {
      this.isSmartMode = this.$refs.chatInputRef.isSmartMode;
      text = text?.trim() || '';
      if (!text) return;
      const render = this.isSmartMode ? 'markdown' : 'html'
      // this.messages.push({ role: 'user', text,renderMode: render});
      this.pushMsg('user', text, render)
      this.input = '';
      this.typing = true;
      this.typingText = '';
      if (this.isSmartMode) {
        await this.sendDeepseekMsg(text)
        return
      }
      try {
        const loadingMsgId = this.messages.length
        // this.messages.push(
        //   { role: 'loading', 
        //   text: '',
        // })
        this.pushMsg('loading', '', render)
        const res = await axios.post('/api/ask', null, {
          params: { msg: text }
        });

        // this.messages.splice(loadingMsgId, 1)
        // await this.typeAiText(res.data.res);
        if (res.data.success) {
          this.messages.splice(loadingMsgId, 1)
          // await this.typeAiText(res.data.res)
          await this.typeAiText(res.data.res, render)
        } else {
          this.messages.splice(loadingMsgId, 1)
          console.log(`msg:${res.data.message}`)
          // this.messages.push({ role: 'bug', text: res.data.message })
        }

        this.typing = false;
        this.$nextTick(() => {
          const history = this.$el.querySelector('.chat-history');
          if (history) history.scrollTop = history.scrollHeight;
        });
      } catch (e) {
        this.clearLoadingMessages()
        // this.messages.push({ role: 'ai', text: '网络错误，请稍后重试。' ,red});
        this.pushMsg('ai', '网络错误，请稍后重试。', 'html')
        this.typing = false;
      }
    },
    async typeAiText(text, render) {
      // 这是啥傻逼bug我真他妈服了
      // this.typingText = '';
      // for (let i = 0; i < text.length; i++) {
      //   this.typingText += text[i];
      //   await new Promise(r => setTimeout(r, 18));
      // }
      // this.messages.push({ role: 'ai', text: this.typingText });
      // this.typingText = '';
      this.typingText = text
      //   this.messages.push({ role: 'ai', 
      //   text: this.typingText,
      //   renderMode: render
      // })
      this.pushMsg('ai', this.typingText, render)
      this.typingText = ''
    },
    newTypeAiText(text) {
    }
  }
};
</script>

<style scoped>
/* loading-bubble*/
.loading-bubble {
  align-items: center;
  display: flex;
  gap: 8px;
}

.loading-bubble .loading {
  margin-top: 0;
}

/* loading */
.loading,
.loading>div {
  position: relative;
  box-sizing: border-box;
}

.loading {
  display: block;
  font-size: 0;
  color: #40c057;
}

.loading.la-dark {
  color: #40c057;
}

.loading>div {
  display: inline-block;
  float: none;
  background-color: currentColor;
  border: 0 solid currentColor;
}

.loading {
  width: 40px;
  height: 10px;
}

.loading>div {
  width: 10px;
  height: 10px;
  border-radius: 100%;
}

.loading>div:first-child {
  transform: translateX(0%);
  animation: ball-newton-cradle-left 1s 0s ease-out infinite;
}

.loading>div:last-child {
  transform: translateX(0%);
  animation: ball-newton-cradle-right 1s 0s ease-out infinite;
}

.loading.la-sm {
  width: 20px;
  height: 4px;
}

.loading.la-sm>div {
  width: 4px;
  height: 4px;
}

.loading.la-2x {
  width: 80px;
  height: 20px;
}

.loading.la-2x>div {
  width: 20px;
  height: 20px;
}

.loading.la-3x {
  width: 120px;
  height: 30px;
}

.loading.la-3x>div {
  width: 30px;
  height: 30px;
}

@keyframes ball-newton-cradle-left {
  25% {
    transform: translateX(-100%);
    animation-timing-function: ease-in;
  }

  50% {
    transform: translateX(0%);
  }
}

@keyframes ball-newton-cradle-right {
  50% {
    transform: translateX(0%);
  }

  75% {
    transform: translateX(100%);
    animation-timing-function: ease-in;
  }

  100% {
    transform: translateX(0%);
  }
}

/* loading */

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
  -webkit-user-select: none;
  /*webkit浏览器*/
  -moz-user-select: none;
  /*火狐*/
  -ms-user-select: none;
  /*IE10*/
  user-select: none;
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

/* inputchat */
.pre-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 60px);
  /* background: linear-gradient(180deg, #ecf9ee 0%, #d4f0d9 100%); */
  background: #ecf9ee;
  padding: 20px;
}

.pre-chat-msg-h2 {
  font-size: 32px;
}

/* 这是啥bug */
.chat-page {
  min-height: 100vh;
  /* background: linear-gradient(180deg, #ecf9ee 0%, #d4f0d9 100%); */
  background: #ecf9ee;
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