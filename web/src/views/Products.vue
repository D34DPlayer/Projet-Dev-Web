<template>
  <div class="mx-5">
    <H2 class="text-center">Titre</H2>
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
  components: {ItemList},
  name: "ProduitList",
  data: function () {
    return {
      products: [
        {
          id: 0,
          name: "chat",
          categorie: "legume",
          src: ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBggIBwgHBwcIDQ0HBwcHCA8ICQcNFREWFhURFRUYHCggGBolGx8TITEhJSkrLi4uFx8zODMsNygtLisBCgoKBQUFDgUFDisZExkrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAOEA4QMBIgACEQEDEQH/xAAaAAEBAQEBAQEAAAAAAAAAAAAAAQMCBAcF/8QAGxABAQEAAwEBAAAAAAAAAAAAAAECAxFBMRL/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A+GgAAAAAAAAAAAAAAAAAAAAAAAoigsrTGumSyg9H7GPagyAAAAAAAAAAAAAAAAAAAAAAAAAAVAHQ5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAAAAAAAAAAAAAAAAAAAAAAAAAAAABQQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWo6sToEAAAAAAAAAAAAAAAAAAAAAAAAAAABvrLi5e7k4bPGGuOwHmsRtcuLkHA6sp0DkXpAEUBBQEFAQUBBQEFAQUBBQEFAQUBBQH7vN9rybAGG2dQBKgAiUARQBEAAABQBAAPAAAAAAAAFAAAH/2Q==","https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          prix: "pas cher",
        }, {
          id: 1,
          name: "chat",
          categorie: "legume",
          src: ["https://www.paysan-breton.fr/wp-content/uploads/2017/11/viande-hachee.jpg","https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          prix: "pas cher",
        }, {
          id: 2,
          name: "chat",
          categorie: "legume",
          src: ["https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          prix: "pas cher",
        }, {
          id: 3,
          name: "chat",
          categorie: "legume",
          src: ["https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          prix: "pas cher",
        }, {
          id: 4,
          name: "chat",
          categorie: "legume",
          src: ["https://static-cdn.jtvnw.net/jtv_user_pictures/c5be9ad8-95e9-4937-b4b7-e4dd460a6c36-profile_image-70x70.png"],
          prix: "pas cher",
        },
      ],
    };
  },
};
</script>

<style scoped></style>
