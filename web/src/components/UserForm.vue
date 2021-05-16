<template>
  <b-modal
    hide-footer
    size="lg"
    ref="userModal"
    :id="modal"
    :title="`${
      edit
        ? 'Modifier l\'utilisateur ' + user.username
        : 'Ajouter un utilisateur'
    }`"
  >
    <!-- Formulaire pour les utilisateurs -->
    <b-form @submit.prevent="onSubmit">
      <b-alert
        :show="error !== ''"
        @dismissed="error = ''"
        variant="danger"
        dismissible
      >
        {{ error }}
      </b-alert>
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
          required
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
import { BModal, BForm, BAlert, BFormGroup, BFormInput } from "bootstrap-vue";
export default {
  name: "UserForm",
  components: { BModal, BForm, BAlert, BFormGroup, BFormInput },
  props: ["user", "username"],
  data() {
    return {
      edit: false,
      form: {
        username: "",
        email: null,
        password: "",
      },
      error: "",
    };
  },
  computed: {
    modal() {
      return `modal-user-${this.edit ? "edit-" + this.user.username : "add"}`;
    },
  },
  methods: {
    async onSubmit() {
      let response;
      if (this.edit) {
        response = await this.$store.dispatch("users/editUser", [
          this.user.username,
          this.form,
        ]);
      } else {
        response = await this.$store.dispatch("users/createUser", this.form);
      }

      switch (response.status) {
        case 200: // It went OK
          this.form = {
            username: "",
            email: null,
            password: "",
          };
          this.error = "";
          this.$refs.userModal.hide();
          break;
        case 400: // Name already used
          this.error = "Un utilisateur avec ce nom existe déjà.";
          break;
        case 404: // User not found
          await this.$store.dispatch("users/getUsers");
          this.$refs.userModal.hide();
          break;
        default:
          // Unknown error
          this.error = response.data.detail || "Unknown error";
      }
    },
    update(val) {
      if (val) {
        this.edit = true;
        this.$set(this.form, "username", val.username);
        this.$set(this.form, "email", val.email);

        if (val.username === this.username) {
          this.error =
            "Après avoir modifié l'utilisateur en cours, vous devrez vous reconnecter.";
        }
      }
    }
  },
  watch: {
    user(val) {
      this.update(val);
    },
  },
  mounted() {
    this.update(this.user);
  }
};
</script>

<style scoped></style>
