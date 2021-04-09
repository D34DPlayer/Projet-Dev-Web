<template>

  <b-table :items="products" :fields="fields">
    <!-- Bouton détail -->
    <template #cell(detail)="row">
      <b-button size="sm" @click="row.toggleDetails" class="mr-2">
        {{ row.detailsShowing ? 'Cacher' : 'Afficher' }}
      </b-button>
    </template>


    <!-- Checkbox visibilité -->
    <template #cell(visibility)="row">
      <b-form-checkbox switch v-model="row.item.visibility"
                       @change="toggleVisibility(row.item.id, row.item.visibility)"></b-form-checkbox>
    </template>


    <!-- Bouton edit -->
    <template #cell(edit)="row">
      <b-button size="sm" v-b-modal="`modal-edit-${row.item.id}`" class="mr-2">
        <b-icon icon="pencil-square"></b-icon>
      </b-button>
        <ProductForm :product="row.item"/>
    </template>


    <!-- Bouton delete -->
    <template #cell(delete)="row">
      <b-button size="sm" v-b-modal="`modal-delete-${row.item.id}`" class="mr-2">
        <b-icon icon="trash-fill"></b-icon>
      </b-button>
      <b-modal hide-footer :id="`modal-delete-${row.item.id}`" title="Effacer le produit">
        <p>NTM {{ row.item.id }}</p>
      </b-modal>
    </template>


    <!-- Develloppement de détail (dscr img) -->
    <template #row-details="row">
      <b-container>
        {{ row.item.description }}
        <div class="images-container">
          <img v-for="(url, i) in row.item.src" :src="url" :alt="row.item.name" :key="i">
        </div>
      </b-container>
    </template>
  </b-table>

</template>

<script>
import ProductForm from "@/components/ProductForm.vue";

export default {
  components: {ProductForm},
  name: "ProductsAdmin",
  props: ["products"],
  data() {
    return {
      fields: [
        {key: "name", label: "Nom", sortable: true},
        {key: "categorie", label: "Catégorie", sortable: true},
        {key: "price", label: "Prix"},
        {key: "promo_price", label: "Promo"},
        {key: "visibility", label: "Visible"},
        {key: "detail", label: "Détail"},
        {key: "edit", label: "Modifier"},
        {key: "delete", label: "Supprimer"}
      ]
    }
  },
  methods: {
    toggleVisibility(id, visibility) {
      console.log(id, visibility);
    }
  }
}
</script>

<style scoped lang="scss">
.images-container {
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    height: 5rem;
    margin: .7rem;
  }
}
</style>