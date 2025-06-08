<template>
  <div class="bg-white min-h-screen p-4 pt-20">
    <SearchBarDisplay @activate="searchOpen = true" />
    <SearchModal :visible="searchOpen" @close="searchOpen = false" />

    <router-link to="/login">ورود</router-link>

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

    <!-- بخش زیرشاخه‌ها -->
    <div class="mt-6 " v-if="selectedCategory && subcategories[selectedCategory]">
    <h2 class="text-md font-bold text-gray-800 mb-3">{{ selectedCategory }} Services</h2>
    <div class="flex gap-4 overflow-x-auto pb-2 px-1 no-scrollbar">
      <div
        v-for="(sub, idx) in subcategories[selectedCategory]"
        :key="idx"
        :class="[
          'w-[120px] h-[160px] shadow rounded-xl p-4 flex flex-col items-center justify-center border shadow-sm cursor-pointer transition-all duration-300',
          sub.bg,
          sub.border
        ]"
        style="flex: 0 0 auto;"
      >
        <div :class="['mb-2 w-12 h-12 rounded-full flex items-center justify-center', sub.iconBg]">
          <i :class="[sub.icon, sub.iconColor, 'text-2xl']"></i>
        </div>
        <div class="text-center">
          <p :class="[sub.textColor, 'text-sm font-semibold leading-tight']">{{ sub.label }}</p>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<style>
.no-scrollbar::-webkit-scrollbar {
  display: none !important;
}
.no-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;     /* Firefox */
}
</style>

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

const subcategories = {
  Cleaning: [
    {
      label: 'Window Washing',
      icon: 'ph ph-windows-logo',
      bg: 'bg-green-50', border: 'border-green-300',
      iconBg: 'bg-green-100', iconColor: 'text-green-600', textColor: 'text-green-600'
    },
    {
      label: 'Stain Removal',
      icon: 'ph ph-sparkle',
      bg: 'bg-green-50', border: 'border-green-300',
      iconBg: 'bg-green-100', iconColor: 'text-green-600', textColor: 'text-green-600'
    },
    {
      label: 'Deep Cleaning',
      icon: 'ph ph-broom',
      bg: 'bg-green-50', border: 'border-green-300',
      iconBg: 'bg-green-100', iconColor: 'text-green-600', textColor: 'text-green-600'
    },
    {
      label: 'Kitchen Clean',
      icon: 'ph ph-pot',
      bg: 'bg-green-50', border: 'border-green-300',
      iconBg: 'bg-green-100', iconColor: 'text-green-600', textColor: 'text-green-600'
    }
  ],
  Painting: [
    {
      label: 'Wall Painting',
      icon: 'ph ph-paint-brush',
      bg: 'bg-rose-50', border: 'border-rose-300',
      iconBg: 'bg-rose-100', iconColor: 'text-rose-500', textColor: 'text-rose-500'
    },
    {
      label: 'Ceiling Painting',
      icon: 'ph ph-brush-broad',
      bg: 'bg-rose-50', border: 'border-rose-300',
      iconBg: 'bg-rose-100', iconColor: 'text-rose-500', textColor: 'text-rose-500'
    },
    {
      label: 'Door Painting',
      icon: 'ph ph-door',
      bg: 'bg-rose-50', border: 'border-rose-300',
      iconBg: 'bg-rose-100', iconColor: 'text-rose-500', textColor: 'text-rose-500'
    },
    {
      label: 'Furniture Painting',
      icon: 'ph ph-armchair',
      bg: 'bg-rose-50', border: 'border-rose-300',
      iconBg: 'bg-rose-100', iconColor: 'text-rose-500', textColor: 'text-rose-500'
    }
  ],
  Vehicle: [
    {
      label: 'Car Wash',
      icon: 'ph ph-car',
      bg: 'bg-purple-50', border: 'border-purple-300',
      iconBg: 'bg-purple-100', iconColor: 'text-purple-600', textColor: 'text-purple-600'
    },
    {
      label: 'Oil Change',
      icon: 'ph ph-oil-can',
      bg: 'bg-purple-50', border: 'border-purple-300',
      iconBg: 'bg-purple-100', iconColor: 'text-purple-600', textColor: 'text-purple-600'
    },
    {
      label: 'Tire Service',
      icon: 'ph ph-steering-wheel',
      bg: 'bg-purple-50', border: 'border-purple-300',
      iconBg: 'bg-purple-100', iconColor: 'text-purple-600', textColor: 'text-purple-600'
    }
  ],
  Labour: [
    {
      label: 'Moving Help',
      icon: 'ph ph-truck',
      bg: 'bg-blue-50', border: 'border-blue-300',
      iconBg: 'bg-blue-100', iconColor: 'text-blue-500', textColor: 'text-blue-500'
    },
    {
      label: 'Assembly',
      icon: 'ph ph-wrench',
      bg: 'bg-blue-50', border: 'border-blue-300',
      iconBg: 'bg-blue-100', iconColor: 'text-blue-500', textColor: 'text-blue-500'
    },
    {
      label: 'General Help',
      icon: 'ph ph-user',
      bg: 'bg-blue-50', border: 'border-blue-300',
      iconBg: 'bg-blue-100', iconColor: 'text-blue-500', textColor: 'text-blue-500'
    }
  ],
  Electrical: [
    {
      label: 'Wiring',
      icon: 'ph ph-lightning',
      bg: 'bg-yellow-50', border: 'border-yellow-300',
      iconBg: 'bg-yellow-100', iconColor: 'text-yellow-500', textColor: 'text-yellow-500'
    },
    {
      label: 'Lighting',
      icon: 'ph ph-lamp',
      bg: 'bg-yellow-50', border: 'border-yellow-300',
      iconBg: 'bg-yellow-100', iconColor: 'text-yellow-500', textColor: 'text-yellow-500'
    },
    {
      label: 'Power Outlets',
      icon: 'ph ph-plug',
      bg: 'bg-yellow-50', border: 'border-yellow-300',
      iconBg: 'bg-yellow-100', iconColor: 'text-yellow-500', textColor: 'text-yellow-500'
    }
  ]
}
</script>
