<template>
  <b-container>
    <h1>Commentaires</h1>
    <b-table-lite :items="comments" :fields="fields">
      <template #cell(name)="row">
        {{ row.item.name }}
      </template>
    </b-table-lite>
  </b-container>
</template>

<script>
import { BTableLite } from "bootstrap-vue";

export default {
  name: "Comments",

  components: {
    BTableLite,
  },
  data() {
    return {
      fields: [
        { key: "name", label: "Nom", sortable: false, class: "text-center" },
        { key: "seen", label: "Vu", sortable: false, class: "text-center" },
        {
          key: "timestamp",
          label: "Date",
          sortable: false,
          class: "text-center",
        },
      ],
    };
  },
  computed: {
    comments() {
      return this.$store.state.comments.comments;
    },
  },
  mounted() {
    this.$store.dispatch("comments/getComments");
  },
};
</script>

<style scoped></style>
