<template>
  <div class="p-4 max-w-md mx-auto space-y-4">
    <h1 class="text-xl font-bold mb-4">ثبت سفارش جدید</h1>

    <form @submit.prevent="submitOrder" class="space-y-4">

      <label class="block">
        <span class="text-sm">دسته‌بندی خدمت</span>
        <select v-model="category" class="w-full p-2 border rounded">
          <option disabled value="">انتخاب کنید...</option>
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </label>

      <label class="block">
        <span class="text-sm">توضیحات</span>
        <textarea v-model="description" rows="4"
                  class="w-full p-2 border rounded" placeholder="مشکل خود را شرح دهید..." />
      </label>

      <label class="block">
        <span class="text-sm">زمان مناسب مراجعه</span>
        <input type="datetime-local" v-model="preferredTime"
               class="w-full p-2 border rounded" />
      </label>

      <button type="submit"
              class="bg-green-600 text-white px-4 py-2 rounded w-full">
        ثبت سفارش
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const category = ref('')
const description = ref('')
const preferredTime = ref('')

const categories = ['برق‌کاری', 'لوله‌کشی', 'نصب تجهیزات', 'تعمیر کولر', 'سایر']

const submitOrder = () => {
  if (!category.value || !description.value || !preferredTime.value) {
    alert('لطفاً تمام فیلدها را کامل کنید')
    return
  }

  // اینجا بعداً به API ارسال می‌کنیم
  console.log('سفارش جدید ثبت شد:', {
    category: category.value,
    description: description.value,
    preferredTime: preferredTime.value
  })

  alert('سفارش شما با موفقیت ثبت شد ✅')
  router.push('/dashboard/customer')
}
</script>
