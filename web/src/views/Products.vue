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
    <b-pagination
      v-model="currentPage"
      :total-rows="totalProducts"
      :per-page="perPage"
      align="center"
      small
    ></b-pagination>
  </div>
</template>

<script>
import ItemList from "@/components/ItemList.vue";
import { BPagination } from "bootstrap-vue";

export default {
  components: { ItemList, BPagination },
  metaInfo: () => ({
    title: "Nos produits",
    meta: [
      {
        vmid: "title",
        name: "og:title",
        content: "Nos produits",
      },
    ],
  }),
  name: "ProduitList",
  mounted() {
    this.$store.dispatch("products/getProducts", [
      this.$store.state.products.page,
    ]);
  },
  computed: {
    products() {
      return this.$store.state.products.products.filter(
        (product) => product.visibility
      );
    },
    totalProducts() {
      return this.$store.state.products.total_products;
    },
    perPage() {
      return this.$store.state.products.size;
    },
    currentPage: {
      get() {
        return this.$store.state.products.page;
      },
      set(value) {
        this.$store.dispatch("products/getProducts", [value]);
      },
    },
  },
};
</script>

<style scoped></style>
