<template>
  <div id="app">
    <NavBar/>
    <Carousel/>
    <router-view/>
    <Footer/>
  </div>
</template>

<script>
import Carousel from "@/components/Carousel.vue";
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";

export default {
  components: {Carousel, NavBar, Footer},
  metaInfo() {
    const path = this.$route.path;
    const image = require('@/assets/logo.png');
    const domain = process.env.VUE_APP_DOMAIN_NAME;

    return {
      title: 'Boucherie artisanale Leuze, Namur',
      titleTemplate: '%s | Boucherie Vangeebergen : viandes, charcuterie, fromages',
      meta: [
        {
          vmid: 'title',
          property: 'og:title',
          content: 'Boucherie artisanale Leuze, Namur'
        },
        {
          property: 'og:site_name',
          content: 'Boucherie Vangeebergen'
        },
        {
          property: 'og:type',
          content: 'website'
        },
        {
          property: 'og:image',
          content: `https://${domain}${image}`
        },
        {
          property: 'og:url',
          content: `https://${domain}${path}`
        },
        {
          property: 'og:description',
          content: 'Nous vous proposons un large assortiment de viandes de premier choix, savoureuses et saines.'
        },
        {
          property: 'og:locale',
          content: 'fr_FR'
        }
      ]
    }
  }
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
