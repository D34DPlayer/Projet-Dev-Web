<template>
  <div id="app">
    <NavBar />
    <Carousel />
    <router-view />
  </div>
</template>

<script>
import Carousel from "@/components/Carousel.vue";
import NavBar from "@/components/NavBar.vue";

export default {
  components: { Carousel, NavBar },
};
</script>

<style lang="scss">
#app {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}
</style>
