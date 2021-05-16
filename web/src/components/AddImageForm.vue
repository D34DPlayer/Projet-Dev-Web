<template>
  <b-modal
    hide-footer
    size="lg"
    :id="modal"
    ref="imageModal"
    :title="`Ajouter des images à un produit`"
  >
    <b-alert
      :show="alert !== ''"
      variant="danger"
      dissmissable
      @dissmissed="alert = ''"
    >
      {{ alert }}
    </b-alert>
    <!-- Formulaire pour les images -->
    <b-form @submit.prevent="onSubmit">
      <!-- Input Images -->
      <b-form-group label="Images :" label-for="input-images">
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
      <b-button type="submit" variant="primary" block>Ajouter</b-button>
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
  name: "AddImageForm",
  components: {
    BModal,
    BAlert,
    BForm,
    BFormGroup,
    BFormFile,
  },
  props: ["productId"],
  data() {
    return {
      photos: [],
      alert: "",
    };
  },
  computed: {
    modal() {
      return `modal-image-${this.productId}`;
    },
  },
  methods: {
    async onSubmit() {
      if (this.photos.length) {
        let data = new FormData();
        for (let file of this.photos) {
          data.append("files", file);
        }

        let response = await this.$store.dispatch("products/addImages", [
          this.productId,
          data,
        ]);
        switch (response.status) {
          case 200: // It went OK
          case 401: // Invalid token, Vuex will logout
            break;
          default:
            // Unknown error
            this.alert = response.data.detail || "Unknown error";
            return;
        }
      }
      this.$refs.imageModal.hide();
    },
  },
};
</script>

<style scoped>
</style>
