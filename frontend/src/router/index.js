import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ServicesView from '../views/ServicesView.vue'
import ProvidersListView from '../views/ProvidersListView.vue'
import CustomerLayout from '../layouts/CustomerLayout.vue'
import ProviderLayout from '../layouts/ProviderLayout.vue'
import CustomerDashboard from '../views/customer/CustomerDashboard.vue'
import ProviderDashboard from '../views/provider/ProviderDashboard.vue'
import { useUserStore } from '../stores/user'
import LoginView from '../views/auth/LoginView.vue'
import NewOrderView from '../views/customer/NewOrderView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/services', name: 'services', component: ServicesView },
  { path: '/providers', name: 'providers', component: ProvidersListView },
  { path: '/login', name: 'login', component: LoginView },
  {
    path: '/dashboard/customer',
    component: CustomerLayout,
    children: [
      {
        path: '',
        name: 'CustomerDashboard',
        component: CustomerDashboard
      },
      {
        path: '/dashboard/customer/new',
        name: 'NewOrder',
        component: NewOrderView
      },
    ]
  },
  {
    path: '/dashboard/provider',
    component: ProviderLayout,
    children: [
      {
        path: '',
        name: 'ProviderDashboard',
        component: ProviderDashboard
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 👇 اینجا که router ساخته شده، حالا گارد مسیر رو تعریف می‌کنیم
router.beforeEach((to, from, next) => {
  const user = useUserStore()

  const requiresCustomer = to.path.startsWith('/dashboard/customer')
  const requiresProvider = to.path.startsWith('/dashboard/provider')

  if (requiresCustomer && user.role !== 'customer') {
    return next({ name: 'home' })
  }

  if (requiresProvider && user.role !== 'provider') {
    return next({ name: 'home' })
  }

  next()
})

export default router
