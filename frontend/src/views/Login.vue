<template>
  <div class="login">
    <h1 class="title">Sign-in</h1>
    <template v-if="!isConfirmed">
      <form @submit.prevent="submitHandler" class="form">
        <input class="input" v-model="username" placeholder="Username" />
        <input
          class="input"
          v-model="password"
          placeholder="Password"
          type="password"
        />
        <button class="btn" type="submit">Sign-in</button>
      </form>
    </template>
    <template v-else>
      <form @submit.prevent="otpVerify" class="form">
        <input class="input" v-model="otpNumber" placeholder="Enter code" />
        <button class="btn" type="submit">Send</button>
      </form>
    </template>
  </div>
</template>

<script>
import config from "../app.config";
import axios from "axios";
axios.defaults.withCredentials = true;
export default {
  name: "Login",
  data() {
    return {
      username: null,
      password: null,
      isConfirmed: false,
      otpNumber: null,
    };
  },
  methods: {
    submitHandler() {
      const user = {
        username: this.username,
        password: this.password,
      };
      fetch(config.host + "/api/v1/account/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
      }).then((response) => {
        if (response.status === 200) {
          this.isConfirmed = true;
          return response.json();
        } else {
          throw new Error(`Got back ${response.status}`);
        }
      });
    },
    cookieShow() {
      console.log(document.cookie);
    },
    otpVerify() {
      const user = {
        username: this.username,
        password: this.password,
        otpNumber: this.otpNumber,
      };
      const response = axios.post(
        config.host + "/api/v1/account/login/verify/",
        user,
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(response);
    },
  },
};
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
.btn {
  font-size: 16px;
  padding: 10px;
  transition: 0.3s;
  border: 1px #2c3e50 solid;
}
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.form {
  display: flex;
  flex-direction: column;
  max-width: 200px;
}
</style>
