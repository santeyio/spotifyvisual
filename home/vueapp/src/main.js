import Vue from 'vue';
import App from './App.vue';
import VueCookie from 'vue-cookie';

Vue.use(VueCookie);

new Vue({
  el: '#app',
  render: h => h(App)
})
