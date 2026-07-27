import { createApp } from 'vue';
import App from './App.vue';
import './assets/styles.css';
import magnetic from './directives/magnetic';

const app = createApp(App);
app.directive('magnetic', magnetic);
app.mount('#app');
