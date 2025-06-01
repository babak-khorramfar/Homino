<template>
  <div
    class="w-full bg-[#f8faff] rounded-xl px-4 py-3 shadow-sm flex items-center gap-2 cursor-pointer"
    :dir="isRtl ? 'rtl' : 'ltr'"
    @click="$emit('activate')"
  >
    <i class="ph ph-magnifying-glass text-gray-400 text-xl"></i>

    <div class="flex items-center gap-1 text-base font-medium text-gray-800 whitespace-nowrap leading-none">
      <span>{{ $t('Search for') }}</span>
      <div class="h-6 overflow-hidden relative w-36">
        <transition-group name="slide" tag="div" class="absolute top-0 left-0">
          <div
            v-for="(term, index) in [currentTerm]"
            :key="index + '-' + term"
            class="slide-item text-pink-600 font-bold text-base"
          >
            {{ term }}...
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const terms = ['Electrical Services', 'Plumbing Services', 'Heating', 'Cooling', 'Safety']
const currentTerm = ref(terms[0])

let index = 0
onMounted(() => {
  setInterval(() => {
    index = (index + 1) % terms.length
    currentTerm.value = terms[index]
  }, 2000)
})
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
</style>
