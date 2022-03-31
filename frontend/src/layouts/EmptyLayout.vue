<template>
  <div class="empty-layout">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "EmptyLayout",
}
</script>

<style scoped>
.empty-layout {
  background: #ddd;
  display: flex;
  position: relative;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>
