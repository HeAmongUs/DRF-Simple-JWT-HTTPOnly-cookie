export default function (instance) {
  return {
    getCurrentUser() {
      return instance.get("api/v1/accounts/user/")
    },
  }
}
