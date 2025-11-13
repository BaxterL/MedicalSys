<template>
  <div class="menu">
    <div class="menu-container">
      <!-- 左侧 Logo 和文字 -->
      <div class="logo-container" @click="goHome">
        <img src="/static/img/Medical_Graph.png" alt="Graph logo" class="logo-icon" />
        <span class="logo-text">医疗助手</span>
      </div>

      <nav class="menu-nav">
        <button class="menu-button" type="button" aria-label="Open menu" @click="toggleDrawer">
          <div class="stripe stripe-1"></div>
          <div class="stripe stripe-2"></div>
          <div class="stripe stripe-3"></div>
        </button>
      </nav>
    </div>

    <!-- 侧边抽屉 -->
    <transition name="drawer">
      <div v-if="isOpen" class="drawer-overlay" @click="closeDrawer">
        <div class="drawer" @click.stop>
          <button class="close-btn" @click="closeDrawer" aria-label="Close menu">✕</button>
          <ul class="drawer-list">
            <li v-for="item in menuItems" :key="item.key" @click="navigate(item)">
              <component :is="item.icon" class="item-icon" />
              <span class="item-text">{{ item.label }}</span>
            </li>
          </ul>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  HomeIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  CodeBracketIcon,
  CircleStackIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const isOpen = ref(false)

const toggleDrawer = () => (isOpen.value = !isOpen.value)
const closeDrawer = () => (isOpen.value = false)

const goHome = () => router.push('/')

const menuItems = [
  { key: 'overview', label: '主页', icon: HomeIcon, path: '/' },
  { key: 'chat', label: '助手', icon: ChatBubbleLeftRightIcon, path: '/chat' },
  { key: 'graph', label: '图谱', icon: ChartBarIcon, path: '/main' },
    {
    key: 'repo',
    label: '代码',
    icon: CodeBracketIcon,
    path: 'https://github.com/BaxterL/MedicalSys',
    external: true
  },
  { key: 'db', label: '数据库', icon: CircleStackIcon, path: 'http://localhost:7474' ,external: true}
]

const navigate = (item) => {
  closeDrawer()
  if (item.external) {
    window.open(item.path, '_blank', 'noopener,noreferrer')
  } else {
    router.push(item.path)
  }
}
</script>

<style scoped>
/* ────────────────────── 基础导航栏 ────────────────────── */
.menu {
  background-color: #e1f6ed;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.menu-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Logo */
.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}
.logo-icon {
  height: 36px;
  width: auto;
  object-fit: contain;
  transition: transform 0.3s ease;
}
.logo-container:hover .logo-icon {
  transform: scale(1.05);
}
.logo-text {
  font-size: 1.4rem;
  font-weight: 600;
  color: #0f172a;
  letter-spacing: 0.5px;
  line-height: 1;
}

/* 汉堡按钮 */
.menu-nav {
  display: flex;
  align-items: center;
}
.menu-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: transparent;
  border: none;
  cursor: pointer;
  height: 30px;
  width: 28px;
  padding: 0;
  transition: all 0.3s ease;
}
.stripe {
  background-color: #334155;
  height: 2.5px;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.7, 0.1, 0.1, 1.5);
}
.stripe-1 { width: 85%; }
.stripe-3 { width: 70%; }
.menu-button:hover .stripe {
  background-color: #00bf63;
  width: 100%;
}

/* ────────────────────── 侧边抽屉 ────────────────────── */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: flex-end;
  z-index: 2000;
}
.drawer {
  background: #ecf9ee;
  width: 180px;
  height: 100%;
  padding: 60px 24px 24px;
  box-shadow: -2px 0 12px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}
.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
}
.drawer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.drawer-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  cursor: pointer;
  transition: color 0.2s;
}
.drawer-list li:hover {
  color: #00bf63;
}
.item-icon {
  width: 20px;
  height: 20px;
  color: currentColor;
}
.item-text {
  font-size: 1rem;
  font-weight: 500;
}

/* 动画 */
.drawer-enter-active,
.drawer-leave-active {
  transition: transform 0.3s ease;
}
.drawer-enter-from,
.drawer-leave-to {
  transform: translateX(100%);
}

@media (max-width: 768px) {
  .menu-container { padding: 0 15px; }
  .logo-text { font-size: 1.2rem; }
  .logo-icon { height: 32px; }
  .drawer { width: 180px; }
}
</style>