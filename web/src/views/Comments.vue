<template>
  <b-container>
    <h1>Commentaires</h1>
    <b-table-lite
        :items="comments"
        :fields="fields"
        @row-clicked="infoComment">
      <template #cell(name)="row">
        <span :class="row.item.seen ? '' : 'puce'">{{ row.item.name }}</span>
      </template>
    </b-table-lite>
    <b-modal
    ok-only
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
      this.$store.commit("comments/seenComment", item.id);
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
    },
    isConnected() {
      return !!this.$store.state.users.user.token;
    },
  },
  watch: {
    isConnected(val) {
      if (!val) this.$router.push("/login");
    },
  },
  mounted() {
    if (!this.isConnected) {
      this.$router.push("/login");
    } else {
      this.$store.dispatch("comments/getComments");
    }
  },
};
</script>


<style>
tbody tr:hover {
  background: rgba(0, 0, 0, 0.05);
}

.label {
  font-weight: bolder;
}
.puce::before {
  content: "●";
  color: var(--primary);
  font-size: 1.5em;
  display: inline-block;
  float: left;
  margin-top: -0.30em;
}
</style>
