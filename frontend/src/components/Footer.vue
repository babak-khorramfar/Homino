<template>
  <footer class="fixed bottom-0 w-full bg-white border-t z-40">
    <div class="relative flex justify-around items-center h-20 px-2">

      <!-- دایره متحرک -->
      <div
        ref="indicator"
        class="absolute -top-5 rounded-full border shadow-lg z-10 transition-all duration-300 ease-in-out flex items-center justify-center"
        :style="{
          left: indicatorLeft + 'px',
          width: active.name === 'home' ? '72px' : '56px',
          height: active.name === 'home' ? '72px' : '56px',
          backgroundColor: '#ec4899'
        }"
      >
        <i :class="[currentIcon, active.name === 'home' ? 'text-3xl' : 'text-2xl', 'text-white']"></i>
      </div>

      <!-- آیتم‌های فوتر -->
      <div
        v-for="(item, index) in items"
        :key="item.name"
        :ref="el => itemRefs[index] = el"
        class="w-1/5 flex flex-col items-center z-20 cursor-pointer"
        @click="activate(item, index)"
      >
        <!-- آیکون -->
        <i
          :class="[item.icon,
            item.name === 'home' ? 'text-3xl' : 'text-lg',
            active.name === item.name ? 'invisible' : 'text-gray-400',
            'transition-all duration-200']"
        ></i>

        <!-- لیبل (مگر Home) -->
        <span
          v-if="item.name !== 'home'"
          class="text-xs transition-all duration-200"
          :class="[
            active.name === item.name ? 'text-pink-600 font-semibold mt-2' : 'text-gray-500 mt-1'
          ]"
        >
          {{ $t(item.label) }}
        </span>
      </div>
    </div>
  </footer>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Footer',
  setup() {
    const route = useRoute()
    const router = useRouter()

    const items = [
        { name: 'services', label: 'Services', path: '/services', icon: 'ph ph-stack' },
        { name: 'orders', label: 'Orders', path: '/orders', icon: 'ph ph-list-bullets' },
        { name: 'home', label: 'Home', path: '/', icon: 'ph ph-house' },
        { name: 'providers', label: 'Top Providers', path: '/providers', icon: 'ph ph-users' },
        { name: 'settings', label: 'Settings', path: '/settings', icon: 'ph ph-gear-six' }
        ]

    const active = ref({ ...items[2] }) // پیش‌فرض: Home
    const currentIcon = ref(active.value.icon)
    const indicator = ref(null)
    const itemRefs = ref([])
    const indicatorLeft = ref(0)

    const moveIndicator = index => {
      const el = itemRefs.value[index]
      if (el && indicator.value) {
        const elRect = el.getBoundingClientRect()
        const parentRect = el.parentElement.getBoundingClientRect()
        const offset = active.value.name === 'home' ? 36 : 28
        indicatorLeft.value = elRect.left - parentRect.left + elRect.width / 2 - offset
      }
    }

    const activate = async (item, index) => {
      active.value = item
      currentIcon.value = item.icon
      await nextTick()
      moveIndicator(index)
      router.push(item.path)
    }

    onMounted(() => {
      const current = items.findIndex(i => i.path === route.path)
      if (current !== -1) {
        activate(items[current], current)
      } else {
        activate(items[2], 2) // fallback: Home
      }
    })

    return {
      items,
      active,
      currentIcon,
      itemRefs,
      indicator,
      indicatorLeft,
      activate
    }
  }
}
</script>

<style scoped>
footer {
  font-family: 'Vazirmatn', sans-serif;
}
</style>
