<template>
  <b-modal
    hide-footer
    size="lg"
    :static="_static"
    :id="modal"
    ref="productModal"
    :title="`${edit ? 'Modifier le' : 'Ajouter un'} produit`"
  >
    <b-alert
      :show="alert != ''"
      variant="danger"
      dissmissable
      @dissmissed="alert = ''"
    >
      {{ alert }}
    </b-alert>
    <!-- Formulaire pour les produits -->
    <b-form @submit.prevent="onSubmit">
      <!-- Input nom de produit -->
      <b-form-group
        label="Nom du produit* :"
        label-for="input-name"
        label-cols-lg
      >
        <b-form-input
          id="input-name"
          v-model="form.name"
          type="text"
          placeholder="Entrez le nom du produit"
          required
        ></b-form-input>
      </b-form-group>
      <!-- Input Catégorie -->
      <b-form-group
        label="Catégorie* :"
        label-for="input-categorie"
        label-cols-lg
      >
        <b-form-input
          id="input-categorie"
          v-model="form.categorie"
          type="text"
          placeholder="Entrez la catégorie"
          required
        ></b-form-input>
      </b-form-group>
      <!-- Input Description -->
      <b-form-group
        label="Description du produit* :"
        label-for="textarea-desc"
        label-cols-lg
      >
        <b-form-textarea
          id="textarea-desc"
          v-model="form.description"
          placeholder="Entrez la description du produit..."
          rows="3"
          max-rows="6"
          required
        ></b-form-textarea>
      </b-form-group>
      <!-- Input Prix -->
      <b-form-group label="Prix* :" label-for="input-prix" label-cols-lg>
        <b-input-group>
          <b-form-input
            min="0"
            step="0.01"
            id="input-prix"
            v-model.number="form.price"
            type="number"
            placeholder="Prix"
            required
          ></b-form-input>
          <b-input-group-text class="input-group-between">
            €
          </b-input-group-text>
          <b-form-select v-model="form.price_type" required>
            <option value="/kilo">/kilo</option>
            <option value="/unité">/unité</option>
          </b-form-select>
        </b-input-group>
      </b-form-group>
      <!-- Input Prix promo -->
      <b-form-group label="Promo :" label-for="input-promo" label-cols-lg>
        <b-input-group>
          <b-form-input
            min="0"
            step="0.01"
            id="input-promo"
            v-model.number="form.promo_price"
            type="number"
            placeholder="Prix promo"
          ></b-form-input>
          <b-input-group-text class="input-group-between">
            €
          </b-input-group-text>
          <b-form-select v-model="form.price_type" disabled>
            <option value="/kilo">/kilo</option>
            <option value="/unité">/unité</option>
          </b-form-select>
        </b-input-group>
      </b-form-group>
      <!-- Input Affichage -->
      <b-form-group
        label="Visibilité :"
        label-for="input-affichage"
        label-class="sr-only"
        class="text-right"
      >
        <b-form-checkbox
          switch
          class="ml-auto"
          id="input-affichage"
          v-model="form.visibility"
          name="checkbox-1"
          value="true"
          unchecked-value="false"
        >
          Afficher dans la liste des produits
        </b-form-checkbox>
      </b-form-group>
      <!-- Input Stock -->
      <b-form-group
        label="En stock :"
        label-for="input-stock"
        label-class="sr-only"
        class="text-right"
      >
        <b-form-checkbox
          switch
          class="ml-auto"
          id="input-stock"
          v-model="form.stock"
          name="checkbox-1"
          value="true"
          unchecked-value="false"
        >
          Le produit est en stock
        </b-form-checkbox>
      </b-form-group>
      <!-- Input Images -->
      <b-form-group label="Images :" label-for="input-images" v-if="!edit">
        <b-form-file
          id="input-images"
          v-model="photos"
          browse-text="Parcourir"
          placeholder="Aucune image sélectionnée"
          drop-placeholder="Déposez les images ici"
          accept="image/*"
          multiple
        ></b-form-file>
      </b-form-group>
      <!-- Bouton submit -->
      <b-button type="submit" variant="primary" block :disabled="inProgress">
        {{edit ? "Modifier" : "Ajouter" }}
      </b-button>
    </b-form>
  </b-modal>
</template>

<script>
import {
  BModal,
  BAlert,
  BForm,
  BFormGroup,
  BFormInput,
  BInputGroup,
  BInputGroupText,
  BFormTextarea,
  BFormSelect,
  BFormCheckbox,
  BFormFile,
} from "bootstrap-vue";
export default {
  name: "ProductForm",
  components: {
    BModal,
    BAlert,
    BForm,
    BFormGroup,
    BFormInput,
    BInputGroup,
    BInputGroupText,
    BFormTextarea,
    BFormSelect,
    BFormCheckbox,
    BFormFile,
  },
  props: { product: Object, _static: { type: Boolean, default: false } },
  data() {
    return {
      form: {
        name: "",
        categorie: "",
        description: "",
        price: null,
        price_type: "/kilo",
        promo_price: null,
        visibility: true,
        stock: true,
      },
      photos: [],
      edit: false,
      alert: "",
      inProgress: false,
    };
  },
  computed: {
    modal() {
      return `modal-${this.edit ? "edit-" + this.product.id : "add"}`;
    },
  },
  watch: {
    product(val) {
      this.update(val);
    },
  },
  mounted() {
    this.update(this.product);
  },
  methods: {
    update(val) {
      if (val) {
        this.$set(this.form, "name", val.name);
        this.$set(this.form, "categorie", val.categorie);
        this.$set(this.form, "description", val.description);
        this.$set(this.form, "price", val.price);
        this.$set(this.form, "promo_price", val.promo_price);
        this.$set(this.form, "price_type", val.price_type);
        this.$set(this.form, "visibility", val.visibility);
        this.edit = true;
      }
    },
    async onSubmit() {
      this.inProgress = true;
      let response;
      if (this.edit) {
        response = await this.$store.dispatch("products/editProduct", [
          this.product.id,
          this.form,
        ]);
      } else {
        response = await this.$store.dispatch("products/addProduct", this.form);
      }

      switch (response.status) {
        case 200: // It went OK
          break;
        case 404: // Product not found
          await this.$store.dispatch("products/getProducts", [
            this.$store.state.products.page,
          ]);
          break;
        case 401: // Invalid token, Vuex will logout
          return;
        default:
          // Unknown error
          this.inProgress = false;
          this.alert = response.data.detail || "Unknown error";
          return;
      }

      if (this.photos.length) {
        let data = new FormData();
        for (let file of this.photos) {
          data.append("files", file);
        }

        response = await this.$store.dispatch("products/addImages", [
          response.data.id,
          data,
        ]);
        switch (response.status) {
          case 200: // It went OK
          case 401: // Invalid token, Vuex will logout
            break;
          default:
            // Unknown error
            this.inProgress = false;
            this.alert = response.data.detail || "Unknown error";
            return;
        }
      }
      this.inProgress = false;
      this.$refs.productModal.hide();
    },
  },
};
</script>

<style scoped>
.input-group-between {
  margin-left: -1px;
  margin-right: -1px;
  border-radius: 0;
}
</style>
