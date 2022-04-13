<template>
  <div class="login">
    <h4 class="title">{{ formTitle }}</h4>
    <template v-if="!isConfirmed">
      <form @submit.prevent="loginHandler" class="form">
        <div class="input-field s6">
          <input
            v-model="username"
            id="username"
            type="text"
            class="validate"
          />
          <label for="username">Username</label>
        </div>
        <div class="input-field s6">
          <input
            v-model="password"
            id="password"
            type="password"
            class="validate"
          />
          <label for="password">Password</label>
        </div>
        <button
          class="btn waves-effect waves-light cyan lighten-1"
          type="submit"
        >
          Sign-in
          <i class="material-icons right cyan lighten-1">send</i>
        </button>
      </form>
    </template>
    <template v-else>
      <form @submit.prevent="otpHandler" class="form">
        <div class="input-field s6">
          <input
            v-model="otpNumber"
            id="otpNumber"
            type="number"
            class="validate"
          />
          <label for="otpNumber">Code</label>
        </div>
        <button
          class="btn waves-effect waves-light cyan lighten-1"
          type="submit"
        >
          Send
          <i class="material-icons right">send</i>
        </button>
      </form>
    </template>
  </div>
</template>

<script>
import messages from "@/plugins/messages"

export default {
  name: "Login",
  data() {
    return {
      username: null,
      password: null,
      isConfirmed: false,
      otpNumber: null,
    }
  },
  computed: {
    formTitle() {
      return this.isConfirmed ? "Enter code" : "Sign-in"
    },
  },
  mounted() {
    window.M.updateTextFields()
  },
  beforeUnmount() {
    clearInterval(this.interval)
  },
  methods: {
    async loginHandler() {
      const user = {
        username: this.username,
        password: this.password,
      }
      const response = await this.$api.auth.signIn(user)
      if (response.status === 200) {
        this.isConfirmed = true
      }
    },
    async otpHandler() {
      const user = {
        username: this.username,
        password: this.password,
        otpNumber: this.otpNumber,
      }
      await this.$api.auth.signIn(user)
      await this.$router.push({ name: "Home" })
      this.$message(messages["loginSuccess"])
    },
  },
}
</script>
<style scoped lang="scss">
.title {
  padding: 0;
  margin: 0 0 10px 0;
}
.input {
  margin-bottom: 10px;
  font-size: 16px;
  outline: none;
  transition: 0.3s;
  border: 1px #2c3e50 solid;

  &:hover {
    background: #eee;
  }
}
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 40px;
  border-radius: 10px;
  background: #fff;
}
.form {
  display: flex;
  flex-direction: column;
  max-width: 200px;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}
</style>
