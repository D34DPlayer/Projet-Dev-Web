import axios from "axios";

const state = () => ({
  days: {
    lu: {},
    ma: {},
    me: {},
    je: {},
    ve: {},
    sa: {},
    di: {},
  },
  endpoints: {
    horaire: "/api/horaire",
  },
});

const mutations = {
  updateHoraire(state, payload) {
    state.days = payload;
  },
};

const actions = {
  async getHoraire({ state, commit }) {
    const url = state.endpoints.horaire;

    try {
      let response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
        },
      });
      commit("updateHoraire", response.data);
      return response;
    } catch (e) {
      console.error(e);
      return e.response;
    }
  },
  async editHoraire({ state, commit, dispatch, rootState }, data) {
    const url = state.endpoints.horaire;

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
      dispatch("getHoraire");
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
