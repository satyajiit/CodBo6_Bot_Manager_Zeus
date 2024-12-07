/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from './vuetify'
import pinia from '@/stores'
import router from '@/router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vue3Toastify from 'vue3-toastify';
import '@/assets/styles/global.css';
import 'vue3-toastify/dist/index.css';


export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(Vue3Toastify, {
      autoClose: 3000,
      fontFamily: 'Poppins, sans-serif',
    })
    .use(VueAxios, axios)
    .use(router)
    .use(pinia)
}

