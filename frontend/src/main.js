import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createI18n } from 'vue-i18n'

const messages = {
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

const i18n = createI18n({
  locale: 'fa',
  fallbackLocale: 'en',
  messages
})

createApp(App).use(router).use(i18n).mount('#app')
