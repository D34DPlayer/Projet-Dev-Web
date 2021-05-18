<template>
  <b-form @submit.prevent="onSubmit">
    <b-container>
      <b-row>
        <b-col cols="6">
          <b-form-group
            id="groupe-name"
            label="Nom :"
            label-for="input-name"
            label-class="sr-only"
          >
            <b-form-input
              id="input-name"
              v-model="form.name"
              type="text"
              placeholder="Nom"
              required
            >
            </b-form-input>
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group
            id="groupe-address"
            label="Adresse :"
            label-for="input-address"
            label-class="sr-only"
          >
            <b-form-input
              id="input-adress"
              v-model="form.address"
              type="text"
              placeholder="Adresse"
            >
            </b-form-input>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="6">
          <b-form-group
            id="groupe-telephone"
            label="Telephone :"
            label-for="input-telephone"
            label-class="sr-only"
          >
            <b-form-input
              id="input-telephone"
              v-model="form.telephone"
              type="number"
              placeholder="Tél"
            >
            </b-form-input>
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group
            id="groupe-email"
            label="Adresse email:"
            label-for="input-email"
            label-class="sr-only"
          >
            <b-form-input
              id="input-email"
              v-model="form.email"
              type="email"
              placeholder="Adresse email"
              required
            >
            </b-form-input>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <b-form-group
            id="groupe-comment"
            label="Commentaire:"
            label-for="input-comment"
            label-class="sr-only"
          >
            <b-form-textarea
              id="input-comment"
              v-model="form.comment"
              placeholder="Commentaire"
              rows="3"
              max-rows="10"
              required
            >
            </b-form-textarea>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row align-v="center">
        <b-col cols="9">
          <b-form-checkbox
            id="input-tos"
            v-model="form.tos"
            name="checkbox-1"
            value="true"
            unchecked-value="false"
            required
            >J'ai lu et j'accepte
            <b-link
              href="https://cdnnen.proxi.tools/res/global/html/confidentialites-fr.html"
              target="_blank"
              >les conditions générales d'utilisation</b-link
            >
          </b-form-checkbox>
        </b-col>
        <b-col cols="3" class="text-right">
          <b-button type="submit" variant="primary"> Envoyer </b-button>
        </b-col>
      </b-row>
    </b-container>
  </b-form>
</template>

<script>
import {
  BForm,
  BFormGroup,
  BFormInput,
  BFormTextarea,
  BFormCheckbox,
  BButton,
} from "bootstrap-vue";
export default {
  name: "ContactForm",
  components: {
    BForm,
    BFormGroup,
    BFormInput,
    BFormTextarea,
    BFormCheckbox,
    BButton,
  },
  data() {
    return {
      form: {
        name: "",
        address: "",
        comment: "",
        email: "",
        telephone: null,
        tos: false,
      },
    };
  },
  methods: {
    onSubmit() {
      console.log(this.form);
    },
  },
};
</script>

<style scoped></style>
