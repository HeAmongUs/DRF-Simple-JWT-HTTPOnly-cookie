import instance from "./instance"
import authModule from "./auth"
import userModule from "./user"

export default {
  auth: authModule(instance),
  user: userModule(instance),
}
