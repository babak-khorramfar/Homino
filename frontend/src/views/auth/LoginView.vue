<template>
  <div class="p-6 max-w-sm mx-auto space-y-6">
    <h2 class="text-xl font-bold text-center">ورود یا ثبت‌نام</h2>
    <p class="text-sm text-center text-gray-600">
      کد تأیید به شماره شما ارسال می‌شود. اگر حسابی وجود نداشته باشد، ثبت‌نام انجام می‌شود.
    </p>

    <!-- مرحله اول: شماره تلفن -->
    <form @submit.prevent="sendOtp" v-if="step === 1" class="space-y-4">
      <input v-model="phone" type="text" placeholder="شماره تلفن" class="w-full p-2 border rounded" />
      <button class="bg-blue-600 text-white w-full p-2 rounded" type="submit">
        دریافت کد تأیید
      </button>
    </form>

    <!-- مرحله دوم: کد تأیید + نقش (در صورت نیاز) -->
    <form @submit.prevent="verifyOtp" v-if="step === 2" class="space-y-4">
      <input v-model="otp" type="text" placeholder="کد تأیید" class="w-full p-2 border rounded" />

      <select v-if="requireRole" v-model="role" class="w-full p-2 border rounded">
        <option disabled value="">انتخاب نقش</option>
        <option value="customer">مشتری</option>
        <option value="provider">متخصص</option>
      </select>

      <button class="bg-green-600 text-white w-full p-2 rounded" type="submit">
        تأیید و ورود
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from '@/plugins/axios'

const router = useRouter()
const user = useUserStore()

const step = ref(1)
const phone = ref('')
const otp = ref('')
const role = ref('')
const requireRole = ref(false)

const sendOtp = async () => {
  if (!phone.value) {
    alert('شماره تلفن را وارد کنید')
    return
  }

  try {
    await axios.post('/auth/send-otp/', { phone: phone.value })
    alert('کد تأیید ارسال شد (ماک: 123456)')
    step.value = 2
  } catch (err) {
    alert('ارسال کد تأیید با خطا مواجه شد')
  }
}

const verifyOtp = async () => {
  if (!otp.value) {
    alert('کد تأیید را وارد کنید')
    return
  }

  try {
    const res = await axios.post('/auth/verify-otp/', {
      phone: phone.value,
      otp: otp.value,
      role: requireRole.value ? role.value : undefined
    })

    user.login(res.data.access, res.data.role)
    router.push(res.data.role === 'customer' ? '/dashboard/customer' : '/dashboard/provider')
  } catch (err) {
    const msg = err.response?.data?.detail || 'خطا در تأیید کد'
    alert(msg)

    // اگر نقش لازم باشد ولی ارسال نشده باشد:
    if (msg.includes('نقش') || msg.includes('ثبت‌نام')) {
      requireRole.value = true
    }
  }
}
</script>
