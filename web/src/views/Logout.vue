<template>
  <b-container>
    <p>Déconnexion en cours...</p>
  </b-container>
</template>

<script>
export default {
  mounted() {
    this.$store.commit("users/logout");
    this.$router.push("/");
  },
};
</script>
