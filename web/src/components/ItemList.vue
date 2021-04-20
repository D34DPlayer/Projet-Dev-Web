<template>
  <b-col xl="3" md="4" sm="6" cols="12" class="my-3">
    <b-card tag="article" no-body>
      <b-card-body>
        <b-card-title>{{ product.name }}</b-card-title>
        <b-card-sub-title>{{ product.categorie }}</b-card-sub-title>
        <b-card-text :class="product.promo_price ? 'promo' : ''"
          >{{ (product.promo_price || product.price).toFixed(2) }}€</b-card-text
        >
      </b-card-body>
      <b-aspect
        class="card-image"
        :style="{ backgroundImage: 'url(https://medias.slash-paris.com/media_attachments/images/000/029/359/carre_noir_blackout_tuesday_art-1_medium.jpg?1591355942)' }"
      >
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

.promo {
  color: var(--danger);
  &::before {
    content: "PROMO";
    background: var(--danger);
    border-radius: 0.25rem;
    color: rgba(255, 255, 255, 0.75);
    margin-right: 0.3rem;
    padding: 0.15rem;
  }
}
</style>
