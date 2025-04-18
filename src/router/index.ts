import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CodeResult from '../views/CodeResult.vue'
import abaoutview from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/result',
      name: 'result',
      component: CodeResult,
    },
    //{
     // path: '/about',
      //name: 'about',
     // component: abaoutview,
    //},
  ],
})

export default router
