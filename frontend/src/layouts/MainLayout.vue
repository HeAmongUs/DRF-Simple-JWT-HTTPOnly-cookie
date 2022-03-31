<template>
  <div class="app-main-layout">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from "@/components/app/Navbar"
export default {
  name: "MainLayout",
  components: { Navbar },
  data() {
    return {}
  },
  mounted() {
    this.$store.dispatch("getCurrentUser")
  },
}
</script>

<style scoped></style>
