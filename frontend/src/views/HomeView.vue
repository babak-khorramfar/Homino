<template>
  <div class="bg-white min-h-screen p-4 pt-20">
    <SearchBarDisplay @activate="searchOpen = true" />
    <SearchModal :visible="searchOpen" @close="searchOpen = false" />
    
    <!-- دسته‌بندی خدمات -->
    <div class="mt-6">
      <h2 class="text-sm font-semibold text-gray-800 mb-3">Homino Services</h2>
      <div class="flex gap-4 overflow-x-auto pb-2 px-1 no-scrollbar">
        <div
          v-for="(item, index) in categories"
          :key="index"
          class="flex-shrink-0 w-20 text-center"
        >
          <div :class="['w-20 h-20 mx-auto rounded-full flex items-center justify-center mb-2 shadow-md', item.bg]">
            <i :class="['text-2xl', item.icon, item.color]"></i>
          </div>
          <p class="text-xs text-gray-600 truncate">{{ item.label }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SearchBarDisplay from '../components/SearchBarDisplay.vue'
import SearchModal from '../components/SearchModal.vue'

const searchOpen = ref(false)

const terms = ['خدمات برقکاری ', 'خدمات لوله کشی ', 'خدمات گرمایش ', 'خدمات سرمایش ', 'خدمات ایمنی ']
const currentTerm = ref(terms[0])

let index = 0
onMounted(() => {
  setInterval(() => {
    index = (index + 1) % terms.length
    currentTerm.value = terms[index]
  }, 2000)
})

const categories = [
  { label: "Cleaning", icon: "ph-fill ph-broom", bg: "bg-green-400/20", color: "text-green-600" },
  { label: "Painting", icon: "ph-fill ph-paint-brush", bg: "bg-rose-400/20", color: "text-rose-500" },
  { label: "Vehicle", icon: "ph-fill ph-truck", bg: "bg-purple-400/20", color: "text-purple-600" },
  { label: "Labour", icon: "ph-fill ph-user", bg: "bg-blue-300/20", color: "text-blue-500" },
  { label: "Electrical", icon: "ph-fill ph-lightning", bg: "bg-yellow-300/20", color: "text-yellow-500" }
]
</script>

<style scoped>
.slide-item {
  transition: transform 0.5s ease-in-out;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s ease;
}
.slide-enter-from {
  transform: translateY(100%);
  opacity: 0;
}
.slide-enter-to {
  transform: translateY(0%);
  opacity: 1;
}
.slide-leave-from {
  transform: translateY(0%);
  opacity: 1;
}
.slide-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
