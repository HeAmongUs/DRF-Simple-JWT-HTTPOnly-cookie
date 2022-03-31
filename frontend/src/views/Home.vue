<template>
  <div class="main">This is main page</div>
  <button @click="refresh">REFRESH TOKEN</button>
</template>

<script>
export default {
  name: "Home",
  methods: {
    refresh() {
      this.$api.auth.refreshToken()
    },
  },
}
</script>

<style scoped></style>
