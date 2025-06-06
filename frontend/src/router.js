import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import ServicesView from './views/ServicesView.vue'
import ProvidersListView from './views/ProvidersListView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/services', name: 'services', component: ServicesView },
  { path: '/providers', name: 'providers', component: ProvidersListView },
  // مسیرهای دیگر هم اینجا اضافه می‌شن
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
