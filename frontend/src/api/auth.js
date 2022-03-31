export default function (instance) {
  return {
    signIn(payload) {
      return instance.post("api/v1/accounts/login/", payload)
    },
    signOut() {
      return instance.delete("api/v1/accounts/logout/")
    },
    refreshToken() {
      return instance.post("api/v1/accounts/refresh/")
    },
  }
}
