import axios from "axios";

const state = () => ({
  contact: {
    address: {
      city: "",
      street: "",
    },
    email: "",
    facebook: "",
    phone: {
      mobile: "",
      office: "",
    },
    tva: "",
  },
  endpoints: {
    contact: "/api/contact",
  },
});

const mutations = {
  updateContact(state, payload) {
    state.contact = payload;
  },
};

const actions = {
  async getContact({ state, commit }) {
    const url = state.endpoints.contact;

    try {
      let response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
        },
      });
      commit("updateContact", response.data);
      return response;
    } catch (e) {
      console.error(e);
      return e.response;
    }
  },
  async editContact({ state, commit, dispatch, rootState }, data) {
    const url = state.endpoints.contact;

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
        data: data,
      });
      dispatch("getContact");
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
