<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">داشبورد مشتری</h1>
    <!-- محتوای مشتری -->
  </div>
</template>
<script setup>
import { useUserStore } from '@/stores/user'
const user = useUserStore()

console.log('نقش کاربر:', user.role)
</script>
