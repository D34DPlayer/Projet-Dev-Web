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
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
