<template>
  <b-col xl="3" md="4" sm="6" cols="12" class="my-3">
    <router-link :to="`/products/${product.id}`">
      <b-card tag="article" no-body>
        <b-card-body>
          <b-card-title>{{ product.name }}</b-card-title>
          <b-card-sub-title>{{ product.categorie }}</b-card-sub-title>
          <b-card-text :class="product.promo_price ? 'promo' : ''"
            >{{ (product.promo_price || product.price).toFixed(2) }}€
          </b-card-text>
        </b-card-body>
        <b-aspect
          :class="
            product.photos.length ? 'card-image' : 'card-image img-placeholder'
          "
          :style="imageFound"
        >
        </b-aspect>
      </b-card>
    </router-link>
  </b-col>
</template>

<script>
import {
  BCard,
  BCardBody,
  BCardTitle,
  BCardSubTitle,
  BCardText,
  BAspect,
} from "bootstrap-vue";
export default {
  name: "ItemList",
  components: {
    BCard,
    BCardBody,
    BCardTitle,
    BCardSubTitle,
    BCardText,
    BAspect,
  },
  props: ["product"],
  data() {
    return {
      size: "",
      imageFound: {},
    };
  },
  mounted() {
    if (this.product.photos.length) {
      this.$set(
        this.imageFound,
        "backgroundImage",
        `url(${this.product.photos[0]})`
      );
    }
  },
};
</script>

<style scoped lang="scss">
.img-placeholder {
  background-image: url("~@/assets/imageNotFound.jpg");
}

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
