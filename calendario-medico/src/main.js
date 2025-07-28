
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'        // <-- importa tu router

const app = createApp(App)
app.use(router)                      // <-- monta Vue Router
app.mount('#app')


