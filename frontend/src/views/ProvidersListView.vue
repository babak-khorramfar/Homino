<template>
  <div class="bg-white min-h-screen p-0 pt-4">
    <SearchBarDisplay @activate="searchOpen = true" />
    <SearchModal :visible="searchOpen" @close="searchOpen = false" />

    <div class="top-providers-page px-2">
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-section mb-7"
      >
        <h2 class="category-title text-base font-semibold mb-3 px-1 text-gray-800">
          {{ category.name }}
        </h2>
        <div class="providers-row flex flex-row gap-3 overflow-x-auto hide-scrollbar px-1">
          <div
            v-for="provider in category.providers"
            :key="provider.id"
            class="provider-card flex flex-col items-center bg-white rounded-2xl shadow-lg py-4 px-2 min-w-[110px] max-w-[130px] flex-shrink-0 relative border border-gray-100"
            style="width: 25vw; max-width: 130px;"
          >
            <img
              :src="provider.avatar"
              alt="Avatar"
              class="w-20 h-20 rounded-full object-cover shadow-md border-2 border-white -mt-8 mb-2"
            />
            <div class="font-semibold text-sm mt-1 text-center text-gray-800 leading-tight">
              {{ provider.name }}
            </div>
            <div class="flex items-center justify-center mt-2">
              <span class="text-yellow-400 mr-1">
                <i class="ph ph-star-fill"></i>
              </span>
              <span class="text-xs font-bold text-gray-700">{{ provider.rating }}</span>
            </div>
            <button
              class="mt-3 bg-pink-500 text-white rounded-xl px-3 py-1 text-xs font-medium shadow transition hover:bg-pink-600"
            >
              View Profile
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SearchBarDisplay from '../components/SearchBarDisplay.vue'
import SearchModal from '../components/SearchModal.vue'
const searchOpen = ref(false)
const categories = ref([
  {
    id: 1,
    name: "Electrical",
    providers: [
      { id: 101, name: "Ali Hosseini", rating: 4.9, avatar: "https://i.pravatar.cc/100?img=1" },
      { id: 102, name: "Mehdi Nikoo", rating: 4.7, avatar: "https://i.pravatar.cc/100?img=2" },
      { id: 103, name: "Amir Rahimi", rating: 4.6, avatar: "https://i.pravatar.cc/100?img=3" },
      { id: 104, name: "Zahra Karimi", rating: 4.5, avatar: "https://i.pravatar.cc/100?img=4" },
      { id: 105, name: "Reza Ebrahimi", rating: 4.4, avatar: "https://i.pravatar.cc/100?img=5" }
    ]
  },
  {
    id: 2,
    name: "Plumbing",
    providers: [
      { id: 201, name: "Sara Rezaei", rating: 4.8, avatar: "https://i.pravatar.cc/100?img=6" },
      { id: 202, name: "Ali Afshar", rating: 4.6, avatar: "https://i.pravatar.cc/100?img=7" },
      { id: 203, name: "Maryam Habibi", rating: 4.5, avatar: "https://i.pravatar.cc/100?img=8" },
      { id: 204, name: "Javad Mohammadi", rating: 4.4, avatar: "https://i.pravatar.cc/100?img=9" },
      { id: 205, name: "Niloofar Saberi", rating: 4.3, avatar: "https://i.pravatar.cc/100?img=10" }
    ]
  }
])
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

.provider-card {
  padding-top: 40px;
    
  transition: box-shadow 0.2s, border-color 0.2s;
  box-shadow: 0 2px 12px 0 #f7a3d011;
}
.provider-card:hover {
  box-shadow: 0 6px 16px 0 #f7a3d077;
  border-color: #f472b6;
}

.category-title {
  /* برای تاکید بیشتر میتونی رنگ دسته ها رو متفاوت بذاری */
}
</style>
