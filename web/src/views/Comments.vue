<template>
  <b-container>
    <h1>
      Commentaires
      <b-badge class="main-badge" variant="danger" v-if="unseen">{{ unseen }}</b-badge>
    </h1>
    <b-table-lite
        :items="comments"
        :fields="fields"
        sort-by="timestamp"
        @row-clicked="infoComment">
      <template #head(check)>
        <b-button-group>
          <b-button variant="outline-primary" @click="seenListComment(selected, false)">
            <BIconEnvelope/>
          </b-button>
          <b-button variant="outline-primary" @click="seenListComment(selected, true)">
            <BIconEnvelopeOpen/>
          </b-button>
        </b-button-group>
        <b-button class="ml-2" variant="danger" @click="deleteListComment(selected)">
          <b-icon-trash-fill/>
        </b-button>
      </template>
      <template #cell(seen)="row">
        <BIconEnvelope v-if="!row.item.seen" class="colored" font-scale="1.5"/>
        <BIconEnvelopeOpen v-if="row.item.seen" class="grey" font-scale="1.5"/>
      </template>
      <template #cell(name)="row">
        {{ row.item.name }}
      </template>
      <template #cell(check)="row">
        <b-form-checkbox
            :id="`check${row.item.id}`"
            @change="updateSelect(row.item.id, $event)"
        ></b-form-checkbox>
      </template>
    </b-table-lite>
    <b-modal
        hide-footer
        id="modalComment"
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
          <b-col><span class="label">Addresse:</span> {{ info.address ? info.address : "Pas d'addresse fournie" }}
          </b-col>
        </b-row>
        <b-row>
          <b-col><span class="label">Tel:</span> {{ info.telephone ? info.telephone : "Pas de numéro fourni" }}</b-col>
          <b-col></b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col>
            <div class="label">Commentaire:</div>
            {{ info.comment }}
          </b-col>
        </b-row>
        <b-row class="mt-3">
          <b-col>
            <b-button block :disabled="seenDisable" @click="seenComment(info.id, !info.seen)">
              {{ info.seen ? 'Marquer comme non lu' : 'Marquer comme lu' }}
            </b-button>
          </b-col>
          <b-col>
            <b-button block :disabled="deleteDisable" variant="danger" @click="deleteComment(info.id)">
              Supprimer le commentaire
            </b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-modal>
  </b-container>
</template>

<script>
import {
  BTableLite,
  BModal,
  BIconEnvelope,
  BIconEnvelopeOpen,
  BFormCheckbox,
  BButtonGroup,
  BIconTrashFill
} from "bootstrap-vue";

export default {
  name: "Comments",

  components: {
    BTableLite,
    BModal,
    BIconEnvelope,
    BIconEnvelopeOpen,
    BFormCheckbox,
    BButtonGroup,
    BIconTrashFill
  },
  data() {
    return {
      selected: {},
      fields: [
        {key: "seen", label: "", class: "text-center"},
        {key: "name", label: "Nom", class: "text-center"},
        {
          key: "timestamp",
          label: "Date",
          class: "text-center",
          formatter: "getDate",
        },
        {key: "check", label: "", class: "text-center"},
      ],
      seenDisable: false,
      deleteDisable: false,
    };
  },
  methods: {
    getDate(date) {
      let options = {year: 'numeric', month: 'numeric', day: 'numeric'};
      let newDate = new Date(date);
      return newDate.toLocaleDateString("fr-FR", options);
    },
    updateSelect(id, event) {
      this.selected[id] = event;
    },
    async infoComment(item) {
      this.$store.commit("comments/seenComment", item.id);
      await this.$store.dispatch("comments/getComment", item.id);
      this.$refs.modalComment.show();
    },
    async seenComment(id, seen) {
      let response = await this.$store.dispatch("comments/unseenComment", [id, seen]);

      switch (response.status) {
        case 200: // it went ok
        case 401: // Vuex will logout
          break;
        case 404: // Not found
          await this.$store.dispatch("comments/getComments");
          this.$refs.modalComment.hide();
      }
    },
    async deleteComment(id) {
      let response = await this.$store.dispatch("comments/deleteComment", id);

      switch (response.status) {
        case 200: // it went ok
        case 401: // Vuex will logout
          break;
        case 404: // Not found
          await this.$store.dispatch("comments/getComments");
      }
      this.$refs.modalComment.hide();
    },
    async seenListComment(ids, seen) {
      let listId = Object.keys(ids).filter(k => ids[k]);
      let response = await this.$store.dispatch("comments/unseenListComment", [listId, seen]);

      switch (response.status) {
        case 200: // it went ok
        case 401: // Vuex will logout
          break;
        case 404: // Not found
          await this.$store.dispatch("comments/getComments");
      }
    },
    async deleteListComment(ids) {
      let listId = Object.keys(ids).filter(k => ids[k]).map(k => +k);
      let response = await this.$store.dispatch("comments/deleteListComment", listId);

      for (let comment of this.comments) {
        document.getElementById(`check${comment.id}`).checked = false;
      }

      switch (response.status) {
        case 200: // it went ok
        case 401: // Vuex will logout
          break;
        case 404: // Not found
          await this.$store.dispatch("comments/getComments");
      }
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
    unseen() {
      return this.$store.getters["comments/unreadComments"];
    }
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

.colored {
  color: var(--primary);
}

.grey {
  color: var(--secondary);
}

.label {
  font-weight: bolder;
}

.main-badge {
  font-size: 1rem;
  transform: translateY(-1rem);
}
</style>
