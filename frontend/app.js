import Example from './components/Example.vue'

const { createApp } = Vue;

const app = createApp({});
app.component('example', Example);
app.mount('#app');
