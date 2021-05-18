<template>
  <b-navbar fixed="top" toggleable="lg" type="dark" variant="navbar">
    <b-navbar-brand to="/">
      <img
        src="@/assets/logo.png"
        alt="Boucherie"
        :class="scrollPos ? 'img-logo' : 'img-logo big'"
      />
      Boucherie Vangeebergen
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item to="/" active-class="active" exact right
          >Accueil</b-nav-item
        >
        <b-nav-item to="/products" active-class="active" right
          >Produits</b-nav-item
        >
        <b-nav-item to="/about" active-class="active" right
          >À propos</b-nav-item
        >
        <b-nav-item to="/contact" active-class="active" right
          >Contact</b-nav-item
        >

        <b-nav-item-dropdown v-if="isConnected" right>
          <!-- Using 'button-content' slot -->
          <template #button-content> {{ user }} </template>
          <b-dropdown-item to="/admin">
            Panneau d'administration
          </b-dropdown-item>
          <b-dropdown-item to="/comments">
            Commentaires <b-badge variant="danger" v-if="unseen">{{ unseen }}</b-badge>
          </b-dropdown-item>
          <b-dropdown-item href="/api/docs">
            Documentation API
          </b-dropdown-item>
          <b-dropdown-item to="/logout">Se déconnecter</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item v-else to="/login" active-class="active"
          >Se connecter</b-nav-item
        >
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      scrollPos: null,
    };
  },
  computed: {
    isConnected() {
      return !!this.$store.state.users.user.token;
    },
    user() {
      return this.$store.state.users.user.username;
    },
    unseen() {
      return this.$store.getters["comments/unreadComments"];
    },
    comments() {
      return this.$store.state.comments.comments.length;
    }
  },
  methods: {
    updateScroll() {
      this.scrollPos = window.scrollY;
    },
  },
  mounted() {
    window.addEventListener("scroll", this.updateScroll);
    if (this.isConnected) {
      this.$store.dispatch("comments/getComments");
    }
  },
};
</script>

<style scoped lang="scss">
.active {
  color: #fff;
}
.img-logo {
  width: 3rem;
  height: auto;
  transition: width 0.4s;
}
.big {
  width: 6rem;
}
.badge {
  transform: translateY(-.15rem);
}
</style>
