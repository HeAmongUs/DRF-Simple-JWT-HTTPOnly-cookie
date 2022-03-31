import { createApp } from "vue"
import App from "./App.vue"
import "./registerServiceWorker"
import router from "./router"
import store from "./store"

import plugins from "./plugins"

import "materialize-css"
const app = createApp(App)
app.use(store).use(router)

plugins.forEach((plugin) => {
  app.use(plugin)
})

app.mount("#app")
