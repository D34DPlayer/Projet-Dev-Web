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
    <h2>Horaires</h2>
    <HoraireForm />
    <hr />
    <h2>Informations de contact</h2>
    <ContactAdmin />
  </b-container>
</template>

<script>
import ProductsAdmin from "@/components/ProductsAdmin.vue";
import ProductForm from "@/components/ProductForm.vue";
import UsersAdmin from "@/components/UsersAdmin.vue";
import UserForm from "@/components/UserForm.vue";
import HoraireForm from "@/components/HoraireForm.vue";
import ContactAdmin from "@/components/ContactAdmin.vue";
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
  components: {
    ProductsAdmin,
    ProductForm,
    UsersAdmin,
    UserForm,
    HoraireForm,
    ContactAdmin,
  },
  directives: { "b-modal": VBModal },
  computed: {
    isConnected() {
      return !!this.$store.state.users.user.token;
    },
    users() {
      return this.$store.state.users.users;
    },
    products() {
      return this.$store.state.products;
    },
  },
  watch: {
    isConnected(val) {
      if (!val) this.$router.push("/login");
    },
  },
  async mounted() {
    if (!this.isConnected) {
      await this.$router.push("/login");
    } else {
      this.$store.dispatch("products/getProducts", [
        this.$store.state.products.page,
      ]);
      this.$store.dispatch("users/getUsers");
    }
  },
};
</script>
