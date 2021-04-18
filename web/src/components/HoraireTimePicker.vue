<template>
  <b-col cols="12" lg="6">
    <b-form-group :label="trad[day]" :label-for="`group-${day}`">
      <b-input-group :id="`group-${day}`">
        <b-form-timepicker
          :state="validation"
          :value="value.open"
          :disabled="!valCheck || !value.is_open"
          label-no-time-selected="Ouverture"
          @input="onInput('open', $event)"
        >
        </b-form-timepicker>
        <b-input-group-prepend class="input-group-append" is-text>
          -
        </b-input-group-prepend>
        <b-form-timepicker
          :state="validation"
          :value="value.close"
          label-no-time-selected="Fermeture"
          :disabled="!valCheck || !value.is_open"
          @input="onInput('close', $event)"
        >
        </b-form-timepicker>
        <b-input-group-append is-text>
          <b-form-checkbox
            v-b-tooltip.hover
            switch
            :title="value.is_open ? 'Ouvert' : 'Fermé'"
            :id="`checkbox-${day}`"
            :checked="value.is_open"
            :disabled="!valCheck"
            @input="onInput('is_open', $event)"
          >
          </b-form-checkbox>
          <b-tooltip :target="`checkbox-${day}`" triggers="hover"> </b-tooltip>
        </b-input-group-append>
      </b-input-group>
      <b-form-invalid-feedback :state="validation">
        Plage horaire invalide.
      </b-form-invalid-feedback>
    </b-form-group>
  </b-col>
</template>

<script>
export default {
  name: "HoraireTimePicker",
  props: ["value", "day", "valCheck", "init"],
  data() {
    return {
      trad: {
        lu: "Lundi",
        ma: "Mardi",
        me: "Mercredi",
        je: "Jeudi",
        ve: "Vendredi",
        sa: "Samedi",
        di: "Dimanche",
      },
    };
  },
  methods: {
    onInput(prop, val) {
      let newValue = { ...this.value };

      newValue[prop] = val;

      this.$emit("input", newValue);
    },
  },
  computed: {
    validation() {
      return this.value.is_open ? this.value.close > this.value.open : null;
    },
  },
};
</script>

<style scoped></style>
