<template>
  <b-container>

    <b-row>
      <b-col>
        <div>
          <CarrouselDetail :images="product.photos" :name="product.name"/>
        </div>
      </b-col>
      <b-col>
        <figure>
          <blockquote class="blockquote">
            <p>{{ product.name }}</p>
          </blockquote>
          <figcaption class="blockquote-footer">
            {{ product.categorie }}
          </figcaption>
        </figure>
        <!--<p class="promo">{{ product.promo_price }}$</p>-->
        <!--<h5>{{ product.price }}{{ product.price_type }}</h5>-->
        <h5 :class="product.promo_price ? 'promo' : ''">{{ (product.promo_price || product.price) }}€ {{
            product.price_type
          }}</h5>
      </b-col>
    </b-row>
    <p class="descri">{{ product.description }}</p>

  </b-container>

</template>

<script>
import CarrouselDetail from "@/components/CarrouselDetail";

export default {
  components: {CarrouselDetail},
  name: "Detail",
  mounted() {
    this.$store.dispatch("products/getProductId", this.$route.params.id);
  },
  computed: {
    product() {
      let prod = this.$store.state.products.detailProduct;
      console.log(prod);
      return prod;
    },
  },
}
</script>

<style scoped lang="scss">
.blockquote > p {
  color: var(--primary);
  font-size: 50px;
}
.blockquote-footer {
  color: var(--primary);
  font-size: 20px
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

