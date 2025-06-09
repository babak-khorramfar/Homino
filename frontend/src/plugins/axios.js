import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true // برای ارسال session و cookie (مثلاً برای OTP)
})

export default instance


withCredentials: true