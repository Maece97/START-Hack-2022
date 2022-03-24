import { createApp } from 'vue';
import { createPinia } from 'pinia';
import VueWordCloud from 'vuewordcloud';
import App from './App.vue';
import router from './router';
import './index.css';

createApp(App)
  .use(router)
  .use(createPinia())
  .component(VueWordCloud.name, VueWordCloud)
  .mount('#app');
