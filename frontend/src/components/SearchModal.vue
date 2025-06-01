<template>
  <transition name="slide-up">
    <div v-if="visible" class="fixed inset-0 bg-white z-50 flex flex-col p-4">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <span class="text-lg font-semibold">{{ $t('Search') }}</span>
        <button @click="$emit('close')">
          <i class="ph ph-x text-xl"></i>
        </button>
      </div>

      <!-- Input -->
      <input
        type="text"
        v-model="query"
        :placeholder="$t('Search for anything...')"
        class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
        autofocus
      />
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'
defineProps(['visible'])
const query = ref('')
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s ease;
}
.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
}
.slide-up-enter-to {
  transform: translateY(0%);
  opacity: 1;
}
.slide-up-leave-from {
  transform: translateY(0%);
  opacity: 1;
}
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
