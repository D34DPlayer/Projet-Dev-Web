import Vue from "vue";
import VueMeta from "vue-meta";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import {
  LinkPlugin,
  LayoutPlugin,
  NavbarPlugin,
  ButtonPlugin,
} from "bootstrap-vue";
import "./app.scss";

Vue.use(VueMeta);

Vue.use(NavbarPlugin);
Vue.use(LinkPlugin);
Vue.use(LayoutPlugin);
Vue.use(ButtonPlugin);

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
