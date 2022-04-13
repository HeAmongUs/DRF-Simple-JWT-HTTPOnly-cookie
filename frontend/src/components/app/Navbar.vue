<template>
  <nav>
    <div class="nav-wrapper cyan lighten-1">
      <a href="#" class="left m-left-10 brand-logo logo">LOGO</a>
      <div class="left m-left-10">
        {{ filteredDate }}
      </div>

      <template v-if="isAuth">
        <div class="left m-left-10" style="font-weight: bold">
          {{ username }}
        </div>
      </template>

      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <template v-for="link in links" :key="link.url">
          <li
            :class="{
              active: $route.path === link.url,
            }"
          >
            <router-link :to="{ name: `${link.title}` }">
              {{ link.title }}</router-link
            >
          </li>
        </template>
        <li v-if="isAuth">
          <a @click.prevent="logout">Logout</a>
        </li>
        <li v-else><router-link to="/login">Sign-in</router-link>></li>
      </ul>
    </div>
  </nav>
</template>

<script>
import messages from "../../plugins/messages"

export default {
  name: "Navbar",
  data() {
    return {
      date: new Date(),
      links: [
        { title: "Home", isAuth: false, url: "/" },
        { title: "Chats", isAuth: true, url: "/chats" },
      ],
    }
  },
  computed: {
    filteredDate() {
      const options = {
        day: "2-digit",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }
      return Intl.DateTimeFormat("ru-RU", options).format(new Date(this.date))
    },
    isAuth() {
      return this.$store.getters.userInfo.isAuth
    },
    username() {
      return this.$store.getters.userInfo.username || null
    },
  },
  mounted() {
    this.interval = setInterval(() => {
      this.date = new Date()
    }, 1000)
    window.M.updateTextFields()
  },
  beforeUnmount() {
    clearInterval(this.interval)
  },
  methods: {
    async logout() {
      try {
        await this.$api.auth.logout()
        this.$store.commit("clearUserInfo")
        await this.$router.push({ name: "Login" })
        this.$message(messages["logout"])
      } catch (e) {
        console.log(e)
      }
    },
  },
}
</script>

<style scoped>
.logo {
  position: relative;
}
.m-left-10 {
  margin-left: 10px;
}
</style>
