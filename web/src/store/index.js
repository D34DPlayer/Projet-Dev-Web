import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import qs from "qs";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    user: {
      token: "",
      username: "",
      email: "",
    },
    endpoints: {
      userData: "/api/users/me",
      login: "/api/token",
    },
  },
  mutations: {
    setToken(state, payload) {
      state.user.token = payload.access_token;
    },
    logout(state) {
      state.user.token = "";
      state.user.username = "";
      state.user.email = "";
    },
    updateUser(state, payload) {
      state.user.username = payload.username;
      state.user.email = payload.email;
    },
  },
  actions: {
    async login({ state, commit, dispatch }, form) {
      const url = state.endpoints.login;

      try {
        let response = await axios(url, {
          method: "POST",
          headers: {
            Accept: "*/*",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
          },
          data: qs.stringify(form),
        });
        commit("setToken", response.data);
        dispatch("getUserData");
        return true;
      } catch (e) {
        console.error(e);
        return false;
      }
    },
    async getUserData({ state, commit }) {
      const url = state.endpoints.userData;

      const AuthStr = "Bearer ".concat(state.user.token);

      try {
        let response = await axios(url, {
          method: "GET",
          headers: {
            Accept: "*/*",
            Authorization: AuthStr,
          },
          credentials: "include",
        });
        console.log(response);
        commit("updateUser", response.data);
        return true;
      } catch (e) {
        console.error(e);
        return false;
      }
    },
  },
  modules: {},
});
