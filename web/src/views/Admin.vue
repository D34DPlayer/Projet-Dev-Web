<template>
  <b-container>
    <h1>Panneau d'administration</h1>
    <ProductsAdmin :products="products"/>
    <b-button v-b-modal.modal-add>Ajouter un nouveau produit</b-button>
    <ProductForm :product="null"/>
  </b-container>
</template>

<script>
import ProductsAdmin from "@/components/ProductsAdmin.vue";
import ProductForm from "@/components/ProductForm.vue";

export default {
  name: "Admin",
  components: {ProductsAdmin, ProductForm},
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
          src: ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBggIBwgHBwcIDQ0HBwcHCA8ICQcNFREWFhURFRUYHCggGBolGx8TITEhJSkrLi4uFx8zODMsNygtLisBCgoKBQUFDgUFDisZExkrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAOEA4QMBIgACEQEDEQH/xAAaAAEBAQEBAQEAAAAAAAAAAAAAAQMCBAcF/8QAGxABAQEAAwEBAAAAAAAAAAAAAAECAxFBMRL/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A+GgAAAAAAAAAAAAAAAAAAAAAAAoigsrTGumSyg9H7GPagyAAAAAAAAAAAAAAAAAAAAAAAAAAVAHQ5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAAAAAAAAAAAAAAAAAAAAAAAAAAAABQQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWo6sToEAAAAAAAAAAAAAAAAAAAAAAAAAAABvrLi5e7k4bPGGuOwHmsRtcuLkHA6sp0DkXpAEUBBQEFAQUBBQEFAQUBBQEFAQUBBQH7vN9rybAGG2dQBKgAiUARQBEAAABQBAAPAAAAAAAAFAAAH/2Q==", "https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          price: 10,
          visibility: false,
          description: "Petite description pour faire jolie pour le site, c'est pas très le français"
        }, {
          id: 1,
          name: "chien",
          categorie: "viande",
          src: ["https://www.paysan-breton.fr/wp-content/uploads/2017/11/viande-hachee.jpg", "https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          price: 10,
          visibility: false,
          description: "Petite description pour faire jolie pour le site, c'est pas très le français"
        }, {
          id: 2,
          name: "vache",
          categorie: "boeuf",
          src: ["https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          price: 10,
          visibility: false,
          description: "Petite description pour faire jolie pour le site, c'est pas très le français"
        }, {
          id: 3,
          name: "jambon",
          categorie: "cochon",
          src: ["https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          price: 10,
          visibility: false,
          description: "Petite description pour faire jolie pour le site, c'est pas très le français"
        }, {
          id: 4,
          name: "aile",
          categorie: "poulet",
          src: ["https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          price: 10,
          visibility: false,
          description: "Petite description pour faire jolie pour le site, c'est pas très le français"
        },
      ],
    };
  },
}
</script>
