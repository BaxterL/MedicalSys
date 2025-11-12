<template>
  <div class="homepage">
    <!-- 导航栏 -->
    <Nvabar></Nvabar>
    <!-- 主内容区 -->
    <main class="main-content">
      <section class="hero-section">
        <!-- <p>test</p> -->
        <!-- 真是个草台班子啊 -->
        <div class="content">
          <div>
            <p class="title">智能医疗<span class="highlight">图谱</span>，精准解读健康</p>
            <p class="desc">基于知识图谱的医疗可视化及问答系统，为你量身定制的医疗助手</p>
          </div>
          <div class="button-list">
            <router-link to="/chat" class="btn primary-btn">开始使用</router-link>
            <router-link to="/main" class="btn outline-btn">图谱数据</router-link>
          </div>
        </div>
        <div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import Nvabar from './navbar.vue';

export default {
  name: 'HomePage',
  data() {
    return {
    }
  },
  mounted() {
  },
  components: {
    Nvabar
  },
  methods: {
  }
}
</script>

<style scoped>
@media (max-width: 375px) {
  .title {
    font-size: 22px;
    padding: 0 15px;
  }
  
  .desc {
    font-size: 15px;
    padding: 0 10px;
  }
}

.homepage {
  min-height: 100vh;
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none"><circle cx="20" cy="20" r="1" stroke="%232e7d32" stroke-opacity="0.1"/><circle cx="80" cy="40" r="1" stroke="%232e7d32" stroke-opacity="0.1"/><circle cx="40" cy="80" r="1" stroke="%232e7d32" stroke-opacity="0.1"/></svg>');
  z-index: 1;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.desc {
  font-size: 16px;
  color: #4a7250;
  margin-bottom: 40px;
  line-height: 1.6;
  padding: 0 15px;
}

.primary-btn {
  background: #40c057;
  color: white;
  box-shadow: 0 4px 12px rgba(64, 192, 87, 0.3);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 192, 87, 0.4);
}

/* .outline-btn {
  background-color: transparent;
  color: #2e7d32;
  border: 2px solid #2e7d32;
  backdrop-filter: blur(10px);
}

.outline-btn:hover {
  background-color: rgba(46, 125, 50, 0.1);
  transform: translateY(-2px);
} */

.outline-btn {
  background-color: white;
  color: #555;
  border: 2px solid transparent;
}

.outline-btn:hover {
  background-color: #ecf9ee;
  box-shadow: inset 0 0 0 2px white;
}

.button-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 280px;
}

.btn {
  display: inline-block;
  text-decoration: none;
  padding: 16px 32px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  text-align: center;
  width: 100%;
  border: none;
  cursor: pointer;
}

.highlight {
  color: #339a46;
  font-weight: 700;
}

.title {
  font-size: 24px;
  margin-bottom: 40px;
  line-height: 1.4;
  font-weight: 700;
  color: #1a3b1f;
  padding: 0 20px;
}

.content {
  animation: fadeInUp 1s ease forwards;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  padding: 60px 0 40px;
  position: relative;
  z-index: 2;
}

/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: sans-serif;
  line-height: 1.6;
}

p {
  display: block;
  margin-block-start: 1em;
  margin-block-end: 1em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  unicode-bidi: isolate;
}

/* 主内容区 */
.main-content {
  background-color: #ebfbee;
  /* padding: 60px 0; */
}

.hero-section {
  min-height: 86vh;
  background: linear-gradient(135deg, #ebfbee 0%, #f0f9f1 100%);
  padding: 20px 20px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
</style>