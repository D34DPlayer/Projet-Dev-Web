<template>
  <div class="mx-5">
    <h1 class="text-center">Liste des produits</h1>
    <b-container>
      <b-row>
        <ItemList
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </b-row>
    </b-container>
  </div>
</template>

<script>
import ItemList from "@/components/ItemList.vue";

export default {
  components: { ItemList },
  name: "ProduitList",
  mounted() {
    this.$store.dispatch("products/getProducts");
  },
  computed: {
    products() {
      return this.$store.state.products.products.filter(
        (product) => product.visibility
      );
    },
  },
};
</script>

<style scoped></style>
