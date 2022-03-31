import { createRouter, createWebHistory } from "vue-router"
import api from "../api"

const routes = [
  {
    path: "/",
    name: "Home",
    meta: { layout: "main", auth: true },
    component: () => import("../views/Home"),
  },
  {
    path: "/login",
    name: "Login",
    meta: { layout: "empty", auth: false },
    component: () => import("../views/Login"),
  },
  {
    path: "/chats",
    name: "Chats",
    meta: { layout: "main", auth: true },
    component: () => import("../views/Chats"),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  let currentUser
  try {
    currentUser =
      (await api.user
        .getCurrentUser()
        .then((r) => r.data)
        .catch(() => null)) || null
  } catch (e) {
    console.log("")
  }
  const requireAuth = to.meta.auth

  if (requireAuth && !currentUser) {
    next({ name: "Login" })
  } else {
    next()
  }
})

export default router
