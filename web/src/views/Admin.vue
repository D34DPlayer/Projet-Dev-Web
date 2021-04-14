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

export default {
  name: "Admin",
  components: { ProductsAdmin, ProductForm, UsersAdmin, UserForm, HoraireForm },
  computed: {
    isConnected() {
      return !!this.$store.state.user.token;
    },
  },
  mounted() {
    if (!this.isConnected) {
      this.$router.push("/");
    }
  },
  data() {
    return {
      products: [
        {
          id: 0,
          name: "chat",
          categorie: "legume",
          src: [
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBggIBwgHBwcIDQ0HBwcHCA8ICQcNFREWFhURFRUYHCggGBolGx8TITEhJSkrLi4uFx8zODMsNygtLisBCgoKBQUFDgUFDisZExkrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAOEA4QMBIgACEQEDEQH/xAAaAAEBAQEBAQEAAAAAAAAAAAAAAQMCBAcF/8QAGxABAQEAAwEBAAAAAAAAAAAAAAECAxFBMRL/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A+GgAAAAAAAAAAAAAAAAAAAAAAAoigsrTGumSyg9H7GPagyAAAAAAAAAAAAAAAAAAAAAAAAAAVAHQ5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAAAAAAAAAAAAAAAAAAAAAAAAAAAABQQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWo6sToEAAAAAAAAAAAAAAAAAAAAAAAAAAABvrLi5e7k4bPGGuOwHmsRtcuLkHA6sp0DkXpAEUBBQEFAQUBBQEFAQUBBQEFAQUBBQH7vN9rybAGG2dQBKgAiUARQBEAAABQBAAPAAAAAAAAFAAAH/2Q==",
            "https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png",
          ],
          price: 10,
          price_type: "/kilo",
          visibility: false,
          description:
            "Petite description pour faire jolie pour le site, c'est pas très le français",
          promo_price: null,
        },
        {
          id: 1,
          name: "chien",
          categorie: "viande",
          src: [
            "https://www.paysan-breton.fr/wp-content/uploads/2017/11/viande-hachee.jpg",
            "https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png",
          ],
          price: 10,
          price_type: "/kilo",
          visibility: false,
          description:
            "Petite description pour faire jolie pour le site, c'est pas très le français",
          promo_price: 3,
        },
        {
          id: 2,
          name: "vache",
          categorie: "boeuf",
          src: [
            "https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png",
          ],
          price: 10,
          price_type: "/kilo",
          visibility: false,
          description:
            "Petite description pour faire jolie pour le site, c'est pas très le français",
        },
        {
          id: 3,
          name: "jambon",
          categorie: "cochon",
          src: [
            "https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png",
          ],
          price: 10,
          price_type: "/kilo",
          visibility: false,
          description:
            "Petite description pour faire jolie pour le site, c'est pas très le français",
        },
        {
          id: 4,
          name: "aile",
          categorie: "poulet",
          src: [
            "https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png",
          ],
          price: 10,
          price_type: "/unité",
          visibility: false,
          description:
            "Petite description pour faire jolie pour le site, c'est pas très le français",
        },
      ],
      users: [
        {
          username: "carlos",
          email: "email",
        },
        {
          username: "cyril",
          email: "email3",
        },
        {
          username: "test",
          email: "email2",
        },
        {
          username: "bamboula",
          email: null,
        },
      ],
    };
  },
};
</script>
