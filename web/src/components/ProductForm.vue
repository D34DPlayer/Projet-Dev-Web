<template>
  <b-modal
    hide-footer
    size="lg"
    :id="`modal-${edit ? 'edit-' + product.id : 'add'}`"
    :title="`${edit ? 'Modifier le' : 'Ajouter un'} produit`"
  >
    <!-- Formulaire pour les produits -->
    <b-form @submit="onSubmit">
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
        visibility: false,
      },
      edit: false,
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
      this.edit = true;
    }
  },
  methods: {
    onSubmit(ev) {
      ev.preventDefault();
      console.log(this.form);
      this.$bvModal.hide(
        `modal-${this.edit ? "edit-" + this.product.id : "add"}`
      );
    },
  },
};
</script>

<style scoped></style>
