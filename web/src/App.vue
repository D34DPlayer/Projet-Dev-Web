<template>
  <div id="app">
    <b-navbar sticky toggleable="lg" type="dark" variant="navbar">
      <b-navbar-brand to="/">Boucherie</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item to="/" right>Accueil</b-nav-item>
          <b-nav-item to="/products" right>Produits</b-nav-item>
          <b-nav-item to="/about" right>À propos</b-nav-item>
          <b-nav-item to="/contact" right>Contact</b-nav-item>

          <b-nav-item-dropdown v-if="isConnected" right>
            <!-- Using 'button-content' slot -->
            <template #button-content> User </template>
            <b-dropdown-item to="/admin">
              Panneau d'administration
            </b-dropdown-item>
            <b-dropdown-item href="/api/docs">
              Documentation API
            </b-dropdown-item>
            <b-dropdown-item to="/logout">Se déconnecter</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item v-else to="/login">Se connecter</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view />
  </div>
</template>

<script>
export default {
  methods: {},
  computed: {
    isConnected() {
      return false;
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
