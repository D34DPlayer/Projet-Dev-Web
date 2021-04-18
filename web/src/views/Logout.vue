<template>
  <div>
    <p>Déconnexion en cours...</p>
  </div>
</template>

<script>
export default {
  mounted() {
    this.$store.commit("users/logout");
    this.$router.push("/");
  },
};
</script>
