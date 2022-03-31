import api from "../api"

export default {
  state: {
    userInfo: {
      isAuth: false,
    },
  },
  getters: {
    userInfo: (state) => state.userInfo,
  },
  mutations: {
    setUserInfo(state, info) {
      state.userInfo = info
    },
    clearUserInfo(state) {
      state.userInfo = {
        isAuth: false,
      }
    },
  },
  actions: {
    async getCurrentUser({ commit, getters }) {
      if (!getters.userInfo.username) {
        const currentUser = {
          ...(await api.user.getCurrentUser()).data,
          isAuth: true,
        }
        commit("setUserInfo", currentUser)
      }
      return getters.userInfo
    },
  },
}
