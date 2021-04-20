<template>
  <b-modal
    hide-footer
    size="lg"
    :id="`modal-${edit ? 'edit-' + product.id : 'add'}`"
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
          <b-input-group-prepend class="input-group-append" is-text
            >€</b-input-group-prepend
          >
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
          <b-input-group-prepend class="input-group-append" is-text
            >€</b-input-group-prepend
          >
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
      <!-- Input Images -->
      <b-form-group label="Images :" label-for="input-images">
        <b-form-file
          id="input-images"
          v-model="form.photos"
          browse-text="Parcourir"
          placeholder="Aucune image sélectionnée"
          drop-placeholder="Déposez les images ici"
          accept="image/*"
          multiple
        ></b-form-file>
      </b-form-group>
      <!-- Bouton submit -->
      <b-button type="submit" variant="primary" block>{{
        edit ? "Modifier" : "Ajouter"
      }}</b-button>
    </b-form>
  </b-modal>
</template>

<script>
export default {
  name: "ProductForm",
  props: ["product"],
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
      },
      photos: [],
      edit: false,
      alert: "",
    };
  },
  mounted() {
    if (this.product) {
      this.$set(this.form, "name", this.product.name);
      this.$set(this.form, "categorie", this.product.categorie);
      this.$set(this.form, "description", this.product.description);
      this.$set(this.form, "price", this.product.price);
      this.$set(this.form, "promo_price", this.product.promo_price);
      this.$set(this.form, "price_type", this.product.price_type);
      this.$set(this.form, "visibility", this.product.visibility);
      this.$set(this, "photos", this.product.photos);
      this.edit = true;
    }
  },
  methods: {
    async onSubmit() {
      if (this.edit) {
        this.$bvModal.hide(`modal-edit-${this.product.id}`);
      }
      let response = await this.$store.dispatch(
        "products/addProduct",
        this.form
      );

      switch (response.status) {
        case 200: // It went OK
          break;
        case 401: // Invalid token, Vuex will logout
          return;
        default:
          // Unknown error
          this.alert = response.data.detail;
          this.showAlert = true;
          return;
      }

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
          this.$bvModal.hide("modal-add");
          break;
        default:
          // Unknown error
          this.alert = response.data.detail;
          this.showAlert = true;
      }
    },
  },
};
</script>

<style scoped></style>
