<template>
  <div class="bg-white min-h-screen p-4 pt-20">
    <SearchBarDisplay @activate="searchOpen = true" />
    <SearchModal :visible="searchOpen" @close="searchOpen = false" />

    <!-- دسته‌بندی خدمات -->
    <div class="mt-6">
      <h2 class="text-sm font-semibold text-gray-800 mb-3">Homino Services</h2>
      <div class="flex gap-4 overflow-visible pb-2 px-1 no-scrollbar items-start min-h-[6.5rem]">
        <div
          v-for="(item, index) in categories"
          :key="index"
          :class="[
            'flex-shrink-0 w-20 text-center cursor-pointer transition-all duration-300',
            selectedCategory === item.label ? 'z-10' : ''
          ]"
          @click="selectedCategory = item.label"
        >
          <div
            :class="[
              'w-20 h-20 mx-auto rounded-full flex items-center justify-center mb-2 transition-all duration-300',
              item.bg,
              item.shadow,
              selectedCategory === item.label ? 'scale-110 border-2 ' + item.border : ''
            ]"
          >
            <i :class="['text-2xl', item.icon, item.color]"></i>
          </div>
          <p
            :class="[
              'text-xs text-gray-600 truncate transition-all duration-300',
              selectedCategory === item.label ? 'font-bold text-gray-600' : ''
            ]"
          >
            {{ item.label }}
          </p>
        </div>
      </div>
    </div>

    <!-- زیرشاخه‌ها -->
    <div v-if="selectedCategory" class="mt-8">
      <h3 class="text-sm font-semibold text-gray-800 mb-4">
        {{ selectedCategory }} Services
      </h3>
      <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-4">
        <div
          v-for="(sub, i) in allSubcategories[selectedCategory]"
          :key="i"
          class="rounded-xl p-4 text-center shadow-sm cursor-pointer transition hover:shadow-md"
          :class="sub.bg"
        >
          <i :class="['text-xl mb-2 block', sub.icon, sub.color]"></i>
          <p class="text-sm font-semibold">{{ sub.name }}</p>
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
const selectedCategory = ref(null)

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
  {
    label: "Cleaning",
    icon: "ph-fill ph-broom",
    bg: "bg-green-400/40",
    color: "text-green-600",
    shadow: "shadow-[0_4px_12px_rgba(34,197,94,0.2)]",
    border: "border-green-500"
  },
  {
    label: "Painting",
    icon: "ph-fill ph-paint-brush",
    bg: "bg-rose-400/40",
    color: "text-rose-500",
    shadow: "shadow-[0_4px_12px_rgba(244,63,94,0.2)]",
    border: "border-rose-500"
  },
  {
    label: "Vehicle",
    icon: "ph-fill ph-truck",
    bg: "bg-purple-400/40",
    color: "text-purple-600",
    shadow: "shadow-[0_4px_12px_rgba(192,132,252,0.2)]",
    border: "border-purple-500"
  },
  {
    label: "Labour",
    icon: "ph-fill ph-user",
    bg: "bg-blue-300/40",
    color: "text-blue-500",
    shadow: "shadow-[0_4px_12px_rgba(59,130,246,0.2)]",
    border: "border-blue-500"
  },
  {
    label: "Electrical",
    icon: "ph-fill ph-lightning",
    bg: "bg-yellow-300/40",
    color: "text-yellow-500",
    shadow: "shadow-[0_4px_12px_rgba(250,204,21,0.2)]",
    border: "border-yellow-500"
  }
]

const allSubcategories = {
  Cleaning: [
    { name: 'Deep Cleaning', icon: 'ph ph-broom', bg: 'bg-green-100', color: 'text-green-600' },
    { name: 'Stain Removal', icon: 'ph ph-sparkle', bg: 'bg-green-100', color: 'text-green-600' },
    { name: 'Window Washing', icon: 'ph ph-windows-logo', bg: 'bg-green-100', color: 'text-green-600' },
    { name: 'Kitchen Clean', icon: 'ph ph-cooking-pot', bg: 'bg-green-100', color: 'text-green-600' }
  ],
  Painting: [
    { name: 'Interior Paint', icon: 'ph ph-wall', bg: 'bg-rose-100', color: 'text-rose-600' },
    { name: 'Exterior Paint', icon: 'ph ph-paint-bucket', bg: 'bg-rose-100', color: 'text-rose-600' }
  ],
  Vehicle: [
    { name: 'Car Wash', icon: 'ph ph-car-profile', bg: 'bg-purple-100', color: 'text-purple-600' },
    { name: 'Oil Change', icon: 'ph ph-engine', bg: 'bg-purple-100', color: 'text-purple-600' }
  ],
  Labour: [
    { name: 'Home Helper', icon: 'ph ph-house', bg: 'bg-blue-100', color: 'text-blue-600' },
    { name: 'Mover', icon: 'ph ph-armchair', bg: 'bg-blue-100', color: 'text-blue-600' }
  ],
  Electrical: [
    { name: 'Switch Fixing', icon: 'ph ph-light-switch', bg: 'bg-yellow-100', color: 'text-yellow-600' },
    { name: 'LED Install', icon: 'ph ph-lightbulb', bg: 'bg-yellow-100', color: 'text-yellow-600' }
  ]
}
</script>
