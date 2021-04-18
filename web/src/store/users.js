import axios from "axios";
import qs from "qs";

const state = () => ({
  user: {
    token: "",
    username: "",
    email: "",
  },
  users: [],
  endpoints: {
    userData: "/api/users/me",
    login: "/api/token",
    users: "/api/users",
  },
});

const mutations = {
  setToken(state, payload) {
    state.user.token = payload.access_token;
  },
  logout(state) {
    state.user.token = "";
    state.user.username = "";
    state.user.email = "";
    state.users = [];
  },
  updateUser(state, payload) {
    state.user.username = payload.username;
    state.user.email = payload.email;
  },
  updateUsers(state, payload) {
    state.users = payload;
  },
};

const actions = {
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
      return response;
    } catch (e) {
      console.error(e);
      return e.response;
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
      commit("updateUser", response.data);
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async getUsers({ state, commit }) {
    const url = state.endpoints.users;

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
      commit("updateUsers", response.data);
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async deleteUser({ state, commit, dispatch }, username) {
    if (state.user.username === username) return false;

    const url = `${state.endpoints.users}/${username}`;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      let response = await axios(url, {
        method: "DELETE",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
        },
        credentials: "include",
      });
      dispatch("getUsers");
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async editUser({ state, commit, dispatch }, [username, data]) {
    const url = `${state.endpoints.users}/${username}`;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      let response = await axios(url, {
        method: "PUT",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        credentials: "include",
        data: data,
      });
      if (state.user.username === username) {
        commit("logout");
      } else {
        dispatch("getUsers");
      }
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async createUser({ state, commit, dispatch }, data) {
    const url = state.endpoints.users;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      let response = await axios(url, {
        method: "POST",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        credentials: "include",
        data: data,
      });
      dispatch("getUsers");
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
