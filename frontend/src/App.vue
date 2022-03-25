<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/login">Sign-in</router-link>
  </div>
  <router-view />
</template>

<style lang="scss">
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
</style>
