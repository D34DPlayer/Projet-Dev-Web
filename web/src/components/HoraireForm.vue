<template>
  <b-form>
    <b-alert v-model="showAlert" variant="danger" dismissible>
      {{ alert }}
    </b-alert>
    <b-container>
      <b-row>
        <HoraireTimePicker
          v-for="(val, key) in days"
          :key="key"
          :day="key"
          :init="val"
          v-model="form[key]"
          :val-check="valCheck"
        />
      </b-row>
    </b-container>
    <b-form-checkbox
      id="checkbox-days"
      v-model="valCheck"
      switch
      @change="onChange"
      :disabled="invalidForm"
    >
      Modifier l'heure
    </b-form-checkbox>
  </b-form>
</template>

<script>
import HoraireTimePicker from "@/components/HoraireTimePicker.vue";
import { BForm, BAlert, BFormCheckbox } from "bootstrap-vue";

export default {
  name: "HoraireForm",
  components: { HoraireTimePicker, BForm, BAlert, BFormCheckbox },
  data() {
    return {
      form: {
        lu: {},
        ma: {},
        me: {},
        je: {},
        ve: {},
        sa: {},
        di: {},
      },
      valCheck: false,
      alert: "",
      showAlert: false,
    };
  },
  mounted() {
    this.$set(this.form, "lu", this.days.lu);
    this.$set(this.form, "ma", this.days.ma);
    this.$set(this.form, "me", this.days.me);
    this.$set(this.form, "je", this.days.je);
    this.$set(this.form, "ve", this.days.ve);
    this.$set(this.form, "sa", this.days.sa);
    this.$set(this.form, "di", this.days.di);
  },
  methods: {
    async onChange(ev) {
      if (!ev) {
        let response = await this.$store.dispatch(
          "horaire/editHoraire",
          this.form
        );

        switch (response.status) {
          case 200: // It went OK
          case 401: // Invalid token, Vuex will logout
            break;
          default:
            // Unknown error
            this.alert = response.data.detail;
            this.showAlert = true;
        }
      }
    },
  },
  computed: {
    invalidForm() {
      for (let val of Object.values(this.form)) {
        if (val.is_open && (!val.close || !val.open || val.close <= val.open)) {
          return true;
        }
      }
      return false;
    },
    days() {
      return this.$store.state.horaire.days;
    },
  },
};
</script>

<style scoped></style>
