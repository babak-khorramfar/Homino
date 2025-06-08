<template>
  <div class="p-4 space-y-4">
    <h1 class="text-xl font-bold">سفارش‌های من</h1>

    <router-link
      to="/dashboard/customer/new"
      class="inline-block bg-blue-600 text-white px-4 py-2 rounded">
      + ثبت سفارش جدید
    </router-link>

    <div v-if="orders.length === 0" class="text-gray-500">
      هنوز سفارشی ثبت نکرده‌اید.
    </div>

    <ul v-else class="space-y-3">
      <li v-for="order in orders" :key="order.id" class="p-3 border rounded shadow-sm">
        <div class="font-semibold">{{ order.title }}</div>
        <div class="text-sm text-gray-600">وضعیت: {{ order.status }}</div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// داده تستی – بعداً از API بارگذاری می‌شود
const orders = ref([
  { id: 1, title: 'تعمیر کولر آبی', status: 'در انتظار پیشنهاد' },
  { id: 2, title: 'لوله‌کشی سرویس بهداشتی', status: 'در حال انجام' },
])

const createNewRequest = () => {
  alert('در آینده شما را به فرم ثبت سفارش جدید هدایت می‌کنیم ✅')
}
</script>
