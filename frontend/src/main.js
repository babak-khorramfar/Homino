import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createI18n } from 'vue-i18n'
import { createPinia } from 'pinia'

// اضافه کردن axios
import axios from '@/plugins/axios'

const i18n = createI18n({
  locale: 'fa',
  fallbackLocale: 'en',
  messages: {
    fa: {
      home: 'خانه',
      services: 'خدمات',
      orders: 'سفارشات',
      logout: 'خروج'
    },
    en: {
      home: 'Home',
      services: 'Services',
      orders: 'Orders',
      logout: 'Logout'
    }
  }
})

const app = createApp(App)

app.config.globalProperties.$axios = axios // ثبت axios به‌صورت global

app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
