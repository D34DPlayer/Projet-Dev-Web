<template>
  <b-container>
    <h1>Panneau d'administration</h1>
    <h2>Produits</h2>
    <ProductsAdmin :products="products" />
    <b-button v-b-modal.modal-add>Ajouter un nouveau produit</b-button>
    <ProductForm :product="null" />
    <hr />
    <h2>Utilisateurs</h2>
    <UsersAdmin :users="users" />
    <b-button v-b-modal.modal-user-add>Ajouter un nouvel utilisateur</b-button>
    <UserForm :user="null" />
    <hr />
    <HoraireForm />
  </b-container>
</template>

<script>
import ProductsAdmin from "@/components/ProductsAdmin.vue";
import ProductForm from "@/components/ProductForm.vue";
import UsersAdmin from "@/components/UsersAdmin.vue";
import UserForm from "@/components/UserForm.vue";
import HoraireForm from "@/components/HoraireForm.vue";
import { VBModal } from "bootstrap-vue";

export default {
  name: "Admin",
  metaInfo: {
    title: "Panneau d'administration",
    meta: [
      {
        vmid: "title",
        name: "og:title",
        content: "Panneau d'administration",
      },
    ],
  },
  components: { ProductsAdmin, ProductForm, UsersAdmin, UserForm, HoraireForm },
  directives: { "b-modal": VBModal },
  computed: {
    isConnected() {
      return !!this.$store.state.users.user.token;
    },
    users() {
      return this.$store.state.users.users;
    },
    products() {
      return this.$store.state.products.products;
    },
  },
  watch: {
    isConnected(val) {
      if (!val) this.$router.push("/login");
    },
  },
  mounted() {
    if (!this.isConnected) {
      this.$router.push("/login");
    } else {
      this.$store.dispatch("products/getProducts");
      this.$store.dispatch("users/getUsers");
    }
  },
};
</script>
