import axios from "axios";

const state = () => ({
  endpoints: {
    products: "/api/products",
  },
  products: [],
});

const mutations = {
  updateProduct(state, payload) {
    state.products = payload.sort((a, b) => 2 * (a.username > b.username) - 1);
  },
};

const actions = {
  async addImages({ state, rootState, dispatch }, [productId, form]) {
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
    dispatch("getProducts");
    return result;
  },
  async deleteImage(
    { state, rootState, dispatch, commit },
    [productId, imgUrl]
  ) {
    const url = state.endpoints.products + `/${productId}/images`;
    const AuthStr = "Bearer ".concat(rootState.users.user.token);

    try {
      let result = await axios(url, {
        method: "DELETE",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        credentials: "include",
        data: [imgUrl],
      });
      dispatch("getProducts");
      return result;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("users/logout", null, { root: true });
      }
      return e.response;
    }
  },
  async addProduct({ state, commit, rootState }, data) {
    const url = state.endpoints.products;
    const AuthStr = "Bearer ".concat(rootState.users.user.token);

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
        commit("users/logout", null, { root: true });
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
  async updateVisibility({ state, rootState, dispatch }, [id, visibility]) {
    const url = `${state.endpoints.products}/${id}/visibility`;

    const AuthStr = "Bearer ".concat(rootState.users.user.token);

    try {
      let response = await axios(url, {
        method: "PUT",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        credentials: "include",
        data: { visibility: visibility },
      });
      dispatch("getProducts");
      return response;
    } catch (e) {
      console.error(e);
      return e.response;
    }
  },
  async updateStock({ state, rootState, dispatch }, [id, stock]) {
    const url = `${state.endpoints.products}/${id}/stock`;
    const AuthStr = "Bearer ".concat(rootState.users.user.token);

    try {
      let response = await axios(url, {
        method: "PUT",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        credentials: "include",
        data: { stock: stock },
      });
      dispatch("getProducts");
      return response;
    } catch (e) {
      console.error(e);
      return e.response;
    }
  },
  async deleteProduct({ state, commit, dispatch, rootState }, id) {
    const url = `${state.endpoints.products}/${id}`;
    const AuthStr = "Bearer ".concat(rootState.users.user.token);

    try {
      let response = await axios(url, {
        method: "DELETE",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
        },
        credentials: "include",
      });
      await dispatch("getProducts");
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("users/logout", null, { root: true });
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
