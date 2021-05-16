<template>
  <b-container>
    <b-table striped bordered responsive :items="products" :fields="fields">
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

      <!-- Checkbox stock -->
      <template #cell(stock)="row">
        <b-form-checkbox
          switch
          v-model="row.item.stock"
          @change="toggleStock(row.item.id, row.item.stock)"
        ></b-form-checkbox>
      </template>

      <!-- Bouton edit -->
      <template #cell(edit)="row">
        <b-button block size="sm" v-b-modal="`modal-edit-${row.item.id}`">
          <b-icon-pencil-square />
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
          <b-icon-trash-fill />
        </b-button>
        <b-modal
          @ok="deleteProduct(row.item.id, $event)"
          :id="`modal-delete-${row.item.id}`"
          title="Effacer le produit"
          size="lg"
        >
          <p>Voulez-vous vraiment supprimer le produit {{ row.item.name }} ?</p>
        </b-modal>
      </template>

      <!-- Develloppement de détail (dscr img) -->
      <template #row-details="row">
        <b-container>
          {{ row.item.description }}
          <div class="images-container">
            <div
              class="images-item"
              v-for="(url, i) in row.item.photos"
              :key="i"
            >
              <b-button
                size="sm"
                variant="danger"
                class="image-delete"
                v-b-modal="`modal-delete-${row.item.id}-image-${i}`"
              >
                <b-icon-trash-fill />
              </b-button>
              <img :src="url" :alt="row.item.name" />
              <b-modal
                @ok="deleteImage(row.item.id, url, $event)"
                :id="`modal-delete-${row.item.id}-image-${i}`"
                title="Effacer l'image"
                size="lg"
              >
                <p>
                  Voulez-vous vraiment supprimer cette image du produit
                  {{ row.item.name }} ?
                </p>
                <img class="modal-image" :src="url" :alt="row.item.name" />
              </b-modal>
            </div>
            <b-button pill size="lg" v-b-modal="`modal-image-${row.item.id}`">
              <b-icon-cloud-arrow-up size="lg" />
            </b-button>
            <AddImageForm :productId="row.item.id" />
          </div>
        </b-container>
      </template>
    </b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="my-table"
    ></b-pagination>
  </b-container>
</template>

<script>
import ProductForm from "@/components/ProductForm.vue";
import AddImageForm from "@/components/AddImageForm";
import {
  BTable,
  BPagination,
  BFormCheckbox,
  BModal,
  BIconTrashFill,
  BIconPencilSquare,
  BIconCloudArrowUp,
  VBModal,
} from "bootstrap-vue";

export default {
  components: {
    ProductForm,
    BTable,
    BPagination,
    BFormCheckbox,
    BModal,
    BIconTrashFill,
    BIconPencilSquare,
    BIconCloudArrowUp,
    AddImageForm,
  },
  directives: { "b-modal": VBModal },
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
        {
          key: "stock",
          label: "En stock",
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
    async toggleVisibility(id, visibility) {
      await this.$store.dispatch("products/updateVisibility", [id, visibility]);
    },
    async toggleStock(id, stock) {
      await this.$store.dispatch("products/updateStock", [id, stock]);
    },
    async deleteProduct(id, ev) {
      let response = await this.$store.dispatch("products/deleteProduct", id);

      switch (response.status) {
        case 404: // The product couldn't be found
          await this.$store.dispatch("products/getProducts");
          break;
        case 200: // It went OK
        case 401: // Wrong credentials, the page will redirect itself
          break;
        default:
          // Unknown error
          ev.preventDefault();
          this.deleteAlert = response.data.detail;
          this.showDeleteAlert = true;
      }
    },
    async deleteImage(id, url, ev) {
      let response = await this.$store.dispatch("products/deleteImage", [
        id,
        url,
      ]);

      switch (response.status) {
        case 200: // It went OK
        case 401: // Wrong credentials, the page will redirect itself
          break;
        default:
          // Unknown error
          ev.preventDefault();
          this.deleteAlert = response.data.detail;
          this.showDeleteAlert = true;
      }
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
.images-item {
  position: relative;
}

.image-delete {
  position: absolute;
  top: 0.4rem;
  right: 0.4rem;
  font-size: 0.75em;
}

.modal-image {
  width: 100%;
  height: auto;
}

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
