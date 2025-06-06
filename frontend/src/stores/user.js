import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isCustomer: (state) => state.role === 'customer',
    isProvider: (state) => state.role === 'provider'
  },
  actions: {
    login(token, role) {
      this.token = token
      this.role = role
      localStorage.setItem('token', token)
      localStorage.setItem('role', role)
    },
    logout() {
      this.token = null
      this.role = null
      localStorage.removeItem('token')
      localStorage.removeItem('role')
    }
  }
})
