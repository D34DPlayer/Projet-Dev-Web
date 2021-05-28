<template>
  <div class="mx-5">
    <h1 class="text-center">Liste des produits</h1>
    <b-container>
      <b-form @submit.prevent="search" class="row">
        <b-col lg="9">
          <b-form-input
            id="search"
            minlength="3"
            placeholder="Rechercher un produit"
          >
          </b-form-input>
        </b-col>
        <b-col>
          <b-button type="submit" variant="primary">Rechercher</b-button>
        </b-col>
        <b-col>
          <b-button
            type="button"
            v-if="is_search"
            @click="clear"
            variant="secondary"
          >
            <BIconX />Clear
          </b-button>
        </b-col>
      </b-form>
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
import { BPagination, BFormInput, BForm, BIconX } from "bootstrap-vue";

export default {
  components: { ItemList, BPagination, BForm, BFormInput, BIconX },
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
  data() {
    return {
      search_data: "",
      is_search: false,
    };
  },
  name: "ProduitList",
  mounted() {
    this.$store.dispatch("products/getProducts", [
      this.$store.state.products.page,
    ]);
  },
  methods: {
    search() {
      console.log("ALO");
      const element = document.getElementById("search");
      let data = element.value;

      this.is_search = true;
      this.search_data = data;
      this.$store.dispatch("products/search", [data]);
    },
    clear() {
      this.search_data = "";
      this.is_search = false;
      this.$store.dispatch("products/getProducts", [1]);
    },
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
        if (this.is_search) {
          this.$store.dispatch("products/search", [this.search_data, value]);
        } else {
          this.$store.dispatch("products/getProducts", [value]);
        }
      },
    },
  },
};
</script>

<style scoped></style>
