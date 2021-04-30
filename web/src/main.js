import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "./app.scss";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
  mounted() {
    //So that the prerenderer knows when to take the snapshot
    document.dispatchEvent(new Event("render-event"));
  },
}).$mount("#app");
