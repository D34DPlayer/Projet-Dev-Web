<template>
  <b-container>
    <b-row>
      <b-alert
        :show="alert != ''"
        variant="danger"
        dissmissable
        @dissmissed="alert = ''"
      >
        {{ alert }}
      </b-alert>
    </b-row>
    <b-row>
      <b-form @submit.prevent="onSubmit">
        <b-container>
          <b-row>
            <b-col>
              <b-form-group
                label="Ville :"
                label-for="input-city"
                label-cols-lg
              >
                <b-form-input
                  id="input-city"
                  v-model="form.address.city"
                  type="text"
                  placeholder="Ville"
                  required
                />
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="Rue :"
                label-for="input-street"
                label-cols-lg
              >
                <b-form-input
                  id="input-street"
                  v-model="form.address.street"
                  type="text"
                  placeholder="Adresse"
                  required
                />
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Téléphone portable :"
                label-for="input-mobile"
                label-cols-lg
              >
                <b-form-input
                  id="input-mobile"
                  v-model="form.phone.mobile"
                  type="tel"
                  pattern="[0-9 ]+"
                  placeholder="Numéro de téléphone portable"
                  required
                />
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="Téléphone fixe :"
                label-for="input-office"
                label-cols-lg
              >
                <b-form-input
                  id="input-office"
                  v-model="form.phone.office"
                  type="tel"
                  pattern="[0-9 ]+"
                  placeholder="Numéro de téléphone fixe"
                  required
                />
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Email :"
                label-for="input-email"
                label-cols-lg
              >
                <b-form-input
                  id="input-email"
                  v-model="form.email"
                  type="email"
                  placeholder="Email de contact"
                  required
                />
              </b-form-group>
            </b-col>
            <b-col
              ><b-form-group
                label="N°: TVA"
                label-for="input-tva"
                label-cols-lg
              >
                <b-form-input
                  id="input-tva"
                  v-model="form.tva"
                  type="text"
                  placeholder="N° TVA"
                  required
                />
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Facebook:"
                label-for="input-facebook"
                label-cols-lg
                label-class="small-flex"
              >
                <b-form-input
                  id="input-facebook"
                  v-model="form.facebook"
                  type="text"
                  placeholder="Lien Facebook"
                  pattern="https?:\/\/(www\.)?facebook\.com\/.+"
                  required
                />
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col></b-col>
            <b-col>
              <b-button block type="submit" variant="primary">Valider</b-button>
            </b-col>
            <b-col></b-col>
          </b-row>
        </b-container>
      </b-form>
    </b-row>
  </b-container>
</template>

<script>
import { BForm, BAlert, BFormGroup, BFormInput } from "bootstrap-vue";

export default {
  name: "ContactAdmin",
  components: { BForm, BAlert, BFormGroup, BFormInput },
  data() {
    return {
      form: {
        address: {
          city: "",
          street: "",
        },
        email: "",
        facebook: "",
        phone: {
          mobile: "",
          office: "",
        },
        tva: "",
      },
      alert: "",
    };
  },
  mounted() {
    this.$set(this.form.address, "city", this.contact.address.city);
    this.$set(this.form.address, "street", this.contact.address.street);
    this.$set(this.form, "email", this.contact.email);
    this.$set(this.form, "facebook", this.contact.facebook);
    this.$set(this.form.phone, "mobile", this.contact.phone.mobile);
    this.$set(this.form.phone, "office", this.contact.phone.office);
    this.$set(this.form, "tva", this.contact.tva);
  },
  methods: {
    async onSubmit() {
      let response = await this.$store.dispatch(
        "contact/editContact",
        this.form
      );

      switch (response.status) {
        case 200: // It went OK
        case 401: // Invalid token, Vuex will logout
          break;
        case 422:
          if (response.data.detail.fields) {
            this.alert = response.data.detail.fields.join("\n");
          } else {
            this.alert = response.data.detail;
          }
          break;
        default:
          // Unknown error
          this.alert = response.data.detail;
      }
    },
  },
  computed: {
    contact() {
      return this.$store.state.contact.contact;
    },
  },
};
</script>

<style scoped>
form {
  width: 100%;
}
</style>

<style>
.small-flex {
  flex-basis: calc(25% - 5px);
  flex-grow: 0;
}
</style>
