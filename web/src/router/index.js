import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('../common/index.vue')
      // component: {
      //   default: () => import('../common/index.vue'),
      //   pc: () => import('../pages/index.vue'),
      //   mobile: () => import('../mobile/index.vue')
      // }
    },
    {
      path: '/main',
      name: 'main',
      component: () => import('../pages/main.vue'),
    },
    {
      path: '/introduce',
      name: 'introduce',
      component: () => import('../pages/introduce.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../common/chat.vue'),
    }
    // {
    //   path: '/test',
    //   name: 'test',
    //   component: () => import('../pages/test.vue'),
    // }
  ],
})

export default router
