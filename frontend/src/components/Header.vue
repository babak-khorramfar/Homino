<template>
  <div>
    <!-- HEADER -->
    <header class="bg-white p-4  flex justify-between items-center fixed top-0 left-0 w-full z-50">
      <!-- Logo سمت راست -->
      <img src="/images/logo_homino.png" alt="Homino Logo" class="h-8" />

      <!-- منوی همبرگری سمت چپ -->
      <button @click="sidebarOpen = !sidebarOpen" class="text-gray-700 text-2xl">
        <i class="fas fa-bars"></i>
      </button>
    </header>

    <!-- OVERLAY -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black bg-opacity-30 z-40"
      @click="sidebarOpen = false"
    ></div>

    <!-- SIDEBAR -->
    <aside
      class="fixed top-0 left-0 w-64 h-full bg-white shadow-md z-50 transition-transform duration-300"
      :class="{ '-translate-x-full': !sidebarOpen, 'translate-x-0': sidebarOpen }"
    >
      <div class="p-4 border-b flex gap-3 items-center">
        <img src="/images/profile.jpg" class="w-10 h-10 rounded-full object-cover" alt="Profile">
        <div>
          <p class="font-semibold text-sm">John Doe</p>
          <p class="text-xs text-gray-500">09123456789</p>
        </div>
      </div>
      <div class="p-4">
        <ul class="space-y-3 text-sm text-gray-700">
          <li><a href="#">Settings</a></li>
          <li><a href="#">Notifications</a></li>
        </ul>
      </div>
      <div class="absolute bottom-0 w-full border-t p-4">
        <button class="text-red-600 font-semibold w-full text-left">
          <i class="fas fa-sign-out-alt mr-2"></i> Logout
        </button>
      </div>
    </aside>
  </div>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      sidebarOpen: false
    };
  }
};
</script>
