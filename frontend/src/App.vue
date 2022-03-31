<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script>
import EmptyLayout from "@/layouts/EmptyLayout"
import MainLayout from "@/layouts/MainLayout"

export default {
  components: {
    MainLayout,
    EmptyLayout,
  },
  computed: {
    layout() {
      return (this.$route.meta.layout || "empty") + "-layout"
    },
  },
}
</script>

<style lang="scss">
@import "~materialize-css/dist/css/materialize.min.css";
#app {
  text-align: center;
}
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
</style>
