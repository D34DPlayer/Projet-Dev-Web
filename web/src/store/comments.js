import axios from "axios";

const state = () => ({
  comments: [],
  currentComment: {},
  endpoints: {
    comments: "/api/comments",
  },
});

const mutations = {
  updateComments(state, payload) {
    state.comments = payload.sort(
      (a, b) => 2 * (a.timestamp > b.timestamp) - 1
    );
  },
  updateCurrentComment(state, payload) {
    state.currentComment = payload;
  },
};

const actions = {
  async addComment({ state }, data) {
    const url = state.endpoints.comments;

    try {
      return await axios(url, {
        method: "POST",
        headers: {
          Accept: "*/*",
          "Content-Type": "application/json",
        },
        data: data,
      });
    } catch (e) {
      console.error(e);
      return e.response;
    }
  },
  async getComments({ state, commit, rootState }) {
    const url = state.endpoints.comments;

    const AuthStr = "Bearer ".concat(rootState.users.user.token);

    try {
      let response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
        },
        credentials: "include",
      });
      commit("updateComments", response.data);
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("users/logout", null, { root: true });
      }
      return e.response;
    }
  },
  async getComment({ state, commit, rootState }, id) {
    const url = `${state.endpoints.comments}/${id}`;

    const AuthStr = "Bearer ".concat(rootState.users.user.token);

    try {
      let response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
        },
        credentials: "include",
      });
      commit("updateCurrentComment", response.data);
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("users/logout", null, { root: true });
      }
      return e.response;
    }
  },
  async deleteComment({ state, dispatch, commit, rootState }, id) {
    const url = `${state.endpoints.comments}/${id}`;

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
      dispatch("getComments");
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("users/logout", null, { root: true });
      }
      return e.response;
    }
  },
  async unseenComment({ state, dispatch, commit, rootState }, id) {
    const url = `${state.endpoints.comments}/${id}/seen`;

    const data = { seen: false };

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
      dispatch("getComments");
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
