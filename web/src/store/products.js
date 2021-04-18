import axios from "axios";

const state = () => ({
  endpoints: {
    products: "/api/products",
  },
  products: [],
});

const mutations = {
  updateProduct(state, payload) {
    state.products = payload;
  },
};

const actions = {
  async addProduct({ state, commit, rootState }, data) {
    const url = state.endpoints.products;
    const AuthStr = "Bearer ".concat(rootState.users.user.token);
    data.photos = [];

    try {
      return await axios(url, {
        method: "POST",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        credentials: "include",
        data: data,
      });
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async getProducts({ state, commit }) {
    const url = state.endpoints.products;

    try {
      let response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
        },
      });
      commit("updateProduct", response.data);
      return response;
    } catch (e) {
      console.error(e);
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
