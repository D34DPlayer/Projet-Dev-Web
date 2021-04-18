import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

import users from "./users";
import horaire from "./horaire";
import products from "./products";

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [createPersistedState()],
  modules: { users, horaire, products },
});
