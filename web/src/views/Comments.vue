<template>
  <b-container>
    <h1>Commentaires</h1>
    <b-table-lite
        :items="comments"
        :fields="fields"
        @row-clicked="infoComment">
    </b-table-lite>
    <b-modal
    id="moadalComment"
    ref="modalComment"
    size="lg"
    :title="`Commentaire du ${getDate(info.timestamp)}`">
      <b-container>
        <b-row>
          <b-col><span class="label">Nom:</span> {{ info.name }}</b-col>
          <b-col><span class="label">Date:</span> {{ getDate(info.timestamp) }}</b-col>
        </b-row>
        <b-row>
          <b-col><span class="label">Email:</span> {{ info.email }}</b-col>
          <b-col><span class="label">Addresse:</span> {{ info.address ? info.address : "Pas d'addresse fournie"}}</b-col>
        </b-row>
        <b-row>
          <b-col><span class="label">Tel:</span> {{info.telephone ? info.telephone : "Pas de numéro fourni"}}</b-col>
          <b-col></b-col>
        </b-row>
        <b-row>
          <b-col><div class="label">Commentaire:</div>{{info.comment}}</b-col>
        </b-row>
      </b-container>
    </b-modal>
  </b-container>
</template>

<script>
import { BTableLite, BModal } from "bootstrap-vue";

export default {
  name: "Comments",

  components: {
    BTableLite,
     BModal
  },
  data() {
    return {
      fields: [
        { key: "name", label: "Nom", class: "text-center" },
        { key: "seen", label: "Vu", class: "text-center" },
        {
          key: "timestamp",
          label: "Date",
          class: "text-center",
          formatter: "getDate",
        },
      ],
    };
  },
  methods: {
    getDate(date) {
      let options = {year: 'numeric', month: 'numeric', day: 'numeric'};
      let newDate = new Date(date);
      return newDate.toLocaleDateString("fr-FR", options);
    },
    async infoComment(item) {
      await this.$store.dispatch("comments/getComment",item.id);
      this.$refs.modalComment.show();
    },
  },
  computed: {
    comments() {
      return this.$store.state.comments.comments;
    },
    info() {
      return this.$store.state.comments.currentComment;
    }
  },
  mounted() {
    this.$store.dispatch("comments/getComments");
  },
};
</script>


<style scoped>
.label {
  font-weight: bolder;
}
</style>
