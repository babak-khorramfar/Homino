<template>
  <footer class="fixed bottom-0 w-full bg-white border-t z-50">
    <div class="relative flex justify-around items-center h-20 pt-4">

      <!-- آیکون Home در مرکز -->
      <router-link
        to="/"
        class="absolute -top-6 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center"
      >
        <div
          class="w-14 h-14 rounded-full border border-gray-300 shadow bg-white flex items-center justify-center"
          :class="{ 'bg-pink-600': isActive('/') }"
        >
          <i
            class="fas fa-home text-2xl"
            :class="isActive('/') ? 'text-white' : 'text-pink-600'"
          ></i>
        </div>
      </router-link>

      <!-- آیتم‌های کناری -->
      <div
        v-for="item in sideItems"
        :key="item.name"
        class="w-1/5 flex flex-col items-center justify-end"
      >
        <router-link :to="item.path" class="flex flex-col items-center text-xs">
          <i
            :class="[item.icon, 'text-lg mb-0.5', isActive(item.path) ? 'text-pink-600' : 'text-gray-400']"
          ></i>
          <span :class="isActive(item.path) ? 'text-pink-600 font-semibold' : 'text-gray-500'">
            {{ $t(item.label) }}
          </span>
        </router-link>
      </div>
    </div>
  </footer>
</template>

<script>
import { useRoute } from 'vue-router'

export default {
  name: 'Footer',
  setup() {
    const route = useRoute()

    const sideItems = [
      { name: 'services', label: 'Services', path: '/services', icon: 'fas fa-layer-group' },
      { name: 'orders', label: 'Orders', path: '/orders', icon: 'fas fa-list' },
      { name: 'notifications', label: 'Notifications', path: '/notifications', icon: 'fas fa-bell' },
      { name: 'settings', label: 'Settings', path: '/settings', icon: 'fas fa-cog' }
    ]

    const isActive = (path) => route.path === path

    return {
      sideItems,
      isActive
    }
  }
}
</script>

<style scoped>
/* آیکون و لیبل نزدیک بهم */
footer i {
  margin-bottom: 0.15rem;
}
</style>
