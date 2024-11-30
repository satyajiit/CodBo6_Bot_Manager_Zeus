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

export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(VueAxios, axios)
    .use(router)
    .use(pinia)
}
