<template>
  <b-table striped bordered responsive="true" :items="users" :fields="fields">
    <template #cell(edit)="row">
      <b-button
        block
        size="sm"
        v-b-modal="`modal-user-edit-${row.item.username}`"
      >
        <b-icon icon="pencil-square"></b-icon>
      </b-button>
      <UserForm :user="row.item" />
    </template>

    <template #cell(delete)="row">
      <b-button
        block
        variant="danger"
        size="sm"
        v-b-modal="`modal-user-delete-${row.item.username}`"
      >
        <b-icon icon="trash-fill"></b-icon>
      </b-button>
      <b-modal
        @ok="deleteUser(row.item.username)"
        :id="`modal-user-delete-${row.item.username}`"
        title="Effacer l'utilisateur"
      >
        <p>
          Voulez-vous vraiment supprimer l'utilisateur {{ row.item.username }} ?
        </p>
      </b-modal>
    </template>
  </b-table>
</template>

<script>
import UserForm from "@/components/UserForm.vue";

export default {
  name: "UsersAdmin",
  components: { UserForm },
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
    };
  },
  methods: {
    formatEmail(val) {
      return val || "-----";
    },
    deleteUser(username) {
      console.log(`User ${username} effacé :c`);
    },
  },
};
</script>

<style scoped></style>
