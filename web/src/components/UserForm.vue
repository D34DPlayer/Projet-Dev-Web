<template>
  <b-modal
    hide-footer
    size="lg"
    :id="`modal-user-${edit ? 'edit-' + user.username : 'add'}`"
    :title="`${
      edit
        ? 'Modifier l\'utilisateur ' + user.username
        : 'Ajouter un utilisateur'
    }`"
  >
    <!-- Formulaire pour les utilisateurs -->
    <b-form @submit="onSubmit">
      <!-- Username -->
      <b-form-group
        label="Nom d'utilisateur* :"
        label-for="input-name"
        label-cols-lg
      >
        <b-form-input
          id="input-name"
          v-model="form.username"
          type="text"
          placeholder="Entrez le nom d'utilisateur"
          required
        ></b-form-input>
      </b-form-group>
      <!-- Email -->
      <b-form-group label="Email :" label-for="input-email" label-cols-lg>
        <b-form-input
          id="input-email"
          v-model="form.email"
          type="email"
          placeholder="Entrez l'email"
        ></b-form-input>
      </b-form-group>
      <!-- Password -->
      <b-form-group
        label="Mot de passe* :"
        label-for="input-password"
        label-cols-lg
      >
        <b-form-input
          id="input-password"
          v-model="form.password"
          type="password"
          placeholder="Entrez le mot de passe"
        ></b-form-input>
      </b-form-group>
      <!-- Bouton submit -->
      <b-button type="submit" variant="primary" block
        >{{ edit ? "Modifier" : "Ajouter" }}
      </b-button>
    </b-form>
  </b-modal>
</template>

<script>
export default {
  name: "UserForm",
  props: ["user"],
  data() {
    return {
      edit: false,
      form: {
        username: "",
        email: "",
        password: "",
      },
    };
  },
  methods: {
    onSubmit(ev) {
      ev.preventDefault();
      return false;
    },
  },
  mounted() {
    if (this.user) {
      this.edit = true;
      this.$set(this.form, "username", this.user.username);
      this.$set(this.form, "email", this.user.email);
    }
  },
};
</script>

<style scoped></style>
