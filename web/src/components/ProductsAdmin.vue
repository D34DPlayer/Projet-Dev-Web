<template>
  <b-table
    striped
    bordered
    responsive="true"
    :items="products"
    :fields="fields"
  >
    <!-- Bouton détail -->
    <template #cell(detail)="row">
      <b-button block variant="info" size="sm" @click="row.toggleDetails">
        {{ row.detailsShowing ? "Cacher" : "Afficher" }}
      </b-button>
    </template>

    <!-- Checkbox visibilité -->
    <template #cell(visibility)="row">
      <b-form-checkbox
        switch
        v-model="row.item.visibility"
        @change="toggleVisibility(row.item.id, row.item.visibility)"
      ></b-form-checkbox>
    </template>

    <!-- Bouton edit -->
    <template #cell(edit)="row">
      <b-button block size="sm" v-b-modal="`modal-edit-${row.item.id}`">
        <b-icon icon="pencil-square"></b-icon>
      </b-button>
      <ProductForm :product="row.item" />
    </template>

    <!-- Bouton delete -->
    <template #cell(delete)="row">
      <b-button
        block
        variant="danger"
        size="sm"
        v-b-modal="`modal-delete-${row.item.id}`"
      >
        <b-icon icon="trash-fill"></b-icon>
      </b-button>
      <b-modal
        @ok="deleteProduct(row.item.id)"
        :id="`modal-delete-${row.item.id}`"
        title="Effacer le produit"
      >
        <p>Voulez-vous vraiment supprimer le produit {{ row.item.name }} ?</p>
      </b-modal>
    </template>

    <!-- Develloppement de détail (dscr img) -->
    <template #row-details="row">
      <b-container>
        {{ row.item.description }}
        <div class="images-container">
          <img
            v-for="(url, i) in row.item.src"
            :src="url"
            :alt="row.item.name"
            :key="i"
          />
        </div>
      </b-container>
    </template>
  </b-table>
</template>

<script>
import ProductForm from "@/components/ProductForm.vue";

export default {
  components: { ProductForm },
  name: "ProductsAdmin",
  props: ["products"],
  data() {
    return {
      fields: [
        { key: "name", label: "Nom", sortable: true, class: "text-center" },
        {
          key: "categorie",
          label: "Catégorie",
          sortable: true,
          class: "text-center",
        },
        {
          key: "price",
          label: "Prix",
          formatter: "formatPrice",
          class: "text-center",
        },
        {
          key: "promo_price",
          label: "Promo",
          formatter: "formatPromo",
          tdClass: this.classPromo,
          class: "text-center",
        },
        { key: "price_type", label: "Type", class: "text-center" },
        {
          key: "visibility",
          label: "Visible",
          sortable: true,
          class: "text-center",
        },
        { key: "detail", label: "Détail", class: "text-center" },
        { key: "edit", label: "Modifier", class: "text-center" },
        { key: "delete", label: "Supprimer", class: "text-center" },
      ],
    };
  },
  methods: {
    toggleVisibility(id, visibility) {
      console.log(id, visibility);
    },
    deleteProduct(id) {
      console.log(`${id} effacé.`);
    },
    formatPrice(val) {
      return `${val.toFixed(2)}€`;
    },
    formatPromo(val) {
      return val ? `${val.toFixed(2)}€` : "-----";
    },
    classPromo(val) {
      return val ? "text-danger" : "";
    },
  },
};
</script>

<style scoped lang="scss">
.images-container {
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    height: 5rem;
    margin: 0.7rem;
  }
}
</style>
