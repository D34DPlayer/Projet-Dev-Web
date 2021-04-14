<template>
  <b-col cols="12" lg="6">
    <b-form-group :label="trad[day]" :label-for="`group-${day}`">
      <b-input-group :id="`group-${day}`">
        <b-form-timepicker
          :state="validation"
          :value="value.open"
          :disabled="!valCheck || !value.isOpen"
          @input="onInput('open', $event)"
        >
        </b-form-timepicker>
        <b-input-group-prepend class="input-group-append" is-text>
          -
        </b-input-group-prepend>
        <b-form-timepicker
          :state="validation"
          :value="value.close"
          :disabled="!valCheck || !value.isOpen"
          @input="onInput('close', $event)"
        >
        </b-form-timepicker>
        <b-input-group-append is-text>
          <b-form-checkbox
            v-b-tooltip.hover
            switch
            :title="value.isOpen ? 'Ouvert': 'Fermé'"
            :id="`checkbox-${day}`"
            :checked="value.isOpen"
            :disabled="!valCheck"
            @input="onInput('isOpen', $event)"
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
      let newValue = {...this.value};

      newValue[prop] = val;

      this.$emit("input", newValue);
    },
  },
  computed: {
    validation() {
      return this.value.close > this.value.open;
    },
  },
};
</script>

<style scoped></style>
