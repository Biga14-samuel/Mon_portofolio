import { createApp } from 'vue';
import { inject } from '@vercel/analytics';
import App from './App.vue';
import './assets/styles.css';
import 'vue-sonner/style.css';
import magnetic from './directives/magnetic';

// Inject Vercel Analytics
inject();

const app = createApp(App);
app.directive('magnetic', magnetic);
app.mount('#app');
