<template>
  <b-table striped bordered responsive :items="users" :fields="fields">
    <template #cell(edit)="row">
      <b-button
        block
        size="sm"
        v-b-modal="`modal-user-edit-${row.item.username}`"
      >
        <b-icon-pencil-square />
      </b-button>
      <UserForm :user="row.item" :username="username" />
    </template>

    <template #cell(delete)="row">
      <b-button
        block
        variant="danger"
        size="sm"
        :disabled="row.item.username === username"
        v-b-modal="`modal-user-delete-${row.item.username}`"
      >
        <b-icon-trash-fill />
      </b-button>
      <b-modal
        size="lg"
        v-if="row.item.username !== username"
        @ok="deleteUser(row.item.username, $event)"
        :id="`modal-user-delete-${row.item.username}`"
        title="Effacer l'utilisateur"
      >
        <b-alert v-model="showDeleteAlert" variant="danger" dismissible>
          {{ deleteAlert }}
        </b-alert>
        <p>
          Voulez-vous vraiment supprimer l'utilisateur {{ row.item.username }} ?
        </p>
      </b-modal>
    </template>
  </b-table>
</template>

<script>
import UserForm from "@/components/UserForm.vue";
import {
  BTable,
  BModal,
  BAlert,
  BIconPencilSquare,
  BIconTrashFill,
  VBModal,
} from "bootstrap-vue";

export default {
  name: "UsersAdmin",
  components: {
    UserForm,
    BTable,
    BModal,
    BAlert,
    BIconPencilSquare,
    BIconTrashFill,
  },
  directives: { "b-modal": VBModal },
  props: ["users"],
  data() {
    return {
      fields: [
        {
          key: "username",
          label: "Nom d'utilisateur",
          sortable: true,
          class: "text-center",
        },
        {
          key: "email",
          label: "Email",
          formatter: "formatEmail",
          sortable: true,
          class: "text-center",
        },
        { key: "edit", label: "Modifier", class: "text-center" },
        { key: "delete", label: "Supprimer", class: "text-center" },
      ],
      deleteAlert: "",
      showDeleteAlert: false,
    };
  },
  methods: {
    formatEmail(val) {
      return val || "-----";
    },
    async deleteUser(username, ev) {
      let response = await this.$store.dispatch("users/deleteUser", username);

      switch (response.status) {
        case 404: // The user couldn't be found
          await this.$store.dispatch("users/getUsers");
          break;
        case 200: // It went OK
        case 401: // Wrong credentials, the page will redirect itself
          break;
        default:
          // Unknown error
          ev.preventDefault();
          this.deleteAlert = response.data.detail;
          this.showDeleteAlert = true;
      }
    },
  },
  computed: {
    username() {
      return this.$store.state.users.user.username;
    },
  },
};
</script>

<style scoped></style>
