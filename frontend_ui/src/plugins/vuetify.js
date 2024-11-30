/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import colors from 'vuetify/util/colors'


// Composables
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        variables: {
          fontFamily: 'Poppins, sans-serif',
        },
        colors: {
          primary: colors.cyan.darken4,
          secondary: colors.teal.darken4,
          surface: colors.grey.lighten5,
          pageBackground: "#f5f5f5",
        }
      }
    }
  }
})
