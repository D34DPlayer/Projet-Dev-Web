import axios from "axios";

const state = () => ({
  endpoints: {
    products: "/api/products",
  },
});

const mutations = {};

const actions = {
  async addImages({ state, rootState }, [productId, form]) {
    const url = state.endpoints.products + `/${productId}/images`;
    const AuthStr = "Bearer ".concat(rootState.users.user.token);

    let result = await axios.post(url, form, {
      headers: {
        Accept: "*/*",
        Authorization: AuthStr,
        "Content-Type": "multipart/form-data",
      },
      credentials: "include",
    });

    return result;
  },
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
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
