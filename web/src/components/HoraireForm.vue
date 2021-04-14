<template>
  <b-form>
    <b-container>
      <b-row>
        <HoraireTimePicker
          v-for="(val, key) in hours"
          :key="key"
          :day="key"
          :init="val"
          v-model="form[key]"
          :val-check="valCheck"
        />
      </b-row>
    </b-container>
    <b-form-checkbox
      id="checkbox-hours"
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

export default {
  name: "HoraireForm",
  components: { HoraireTimePicker },
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
      hours: {
        lu: {
          open: "10:00:00",
          close: "12:00:00",
          isOpen: true,
        },
        ma: {
          open: "10:00:00",
          close: "12:00:00",
          isOpen: true,
        },
        me: {
          open: "10:00:00",
          close: "12:00:00",
          isOpen: true,
        },
        je: {
          open: "10:00:00",
          close: "12:00:00",
          isOpen: true,
        },
        ve: {
          open: "10:00:00",
          close: "12:00:00",
          isOpen: true,
        },
        sa: {
          open: "10:00:00",
          close: "12:00:00",
          isOpen: true,
        },
        di: {
          open: "10:00:00",
          close: "13:00:00",
          isOpen: true,
        },
      },
    };
  },
  mounted() {
    this.$set(this.form, "lu", this.hours.lu);
    this.$set(this.form, "ma", this.hours.ma);
    this.$set(this.form, "me", this.hours.me);
    this.$set(this.form, "je", this.hours.je);
    this.$set(this.form, "ve", this.hours.ve);
    this.$set(this.form, "sa", this.hours.sa);
    this.$set(this.form, "di", this.hours.di);
  },
  methods: {
    onChange(ev) {
      if (!ev) {
        console.log(this.form);
      }
    },
  },
  computed: {
    invalidForm() {
      for (let val of Object.values(this.form)) {
        if (val.close <= val.open) {
          return true;
        }
      }
      return false;
    },
  },
};
</script>

<style scoped></style>
