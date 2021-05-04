<template>
  <b-container>
    <p>Déconnexion en cours...</p>
  </b-container>
</template>

<script>
export default {
  metaInfo: {
      title: 'Se déconnecter',
      meta: [
        {
          vmid: 'title',
          name: 'og:title',
          content: 'Se déconnecter'
        }
      ]
  },
  mounted() {
    this.$store.commit("users/logout");
    this.$router.push("/");
  },
};
</script>
