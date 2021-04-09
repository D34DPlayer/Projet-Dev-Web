<template>
  <b-col lg="3" md="4" sm="6" cols="12" class="my-3">
    <b-card
        tag="article"
        no-body
    >
      <b-card-body>
        <b-card-title>{{ product.name }}</b-card-title>
        <b-card-sub-title>{{ product.categorie }}</b-card-sub-title>
        <b-card-text>{{ product.price }}</b-card-text>
      </b-card-body>
      <b-aspect class="card-image" :style="{ backgroundImage: 'url(' + product.src[0] + ')' }">
      </b-aspect>
    </b-card>
  </b-col>
</template>

<script>
export default {
  name: "ItemList",
  props: ["product"],
  data() {
    return {
      size: "",
    };
  },
};
</script>

<style scoped lang="scss">
.card-text {
  position: absolute;
  bottom: 0;
  right: 0;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.75);
  border-radius: 0.25rem 0 0 0;
}

.card-image {
  background-position: center;
  background-size: cover;
}
</style>
