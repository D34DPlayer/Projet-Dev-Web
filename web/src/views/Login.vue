<template>
  <b-container>
    <b-row>
      <b-col sm="9" md="7" lg="5" class="mx-auto mb-5">
        <b-alert v-model="loginAlert" variant="danger" dismissible>
          Mauvaise combinaison de nom d'utilisateur/mot de passe.
        </b-alert>
        <b-card class="login-card">
          <b-form @submit="onSubmit" v-if="!isConnected">
            <b-form-group
              class="w-100"
              label="Nom d'utilisateur :"
              label-for="input-username"
            >
              <b-form-input
                id="input-username"
                v-model="form.username"
                placeholder="Ton nom d'utilisateur"
                required
              ></b-form-input>
            </b-form-group>
            <b-form-group label="Mot de passe :" label-for="input-password">
              <b-form-input
                id="input-password"
                v-model="form.password"
                placeholder="Ton mot de passe"
                type="password"
                required
              ></b-form-input>
            </b-form-group>
            <b-button
              class="mt-4 text-uppercase"
              block
              type="submit"
              variant="primary"
              >Se connecter</b-button
            >
          </b-form>
          <p v-else>Redirecting...</p>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<style scoped lang="scss">
.login-card {
  border: 0;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem 0 rgba(0, 0, 0, 0.1);
}

.card-title {
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 300;
  font-size: 1.5rem;
}

.card-body {
  padding: 2rem;
}

.btn {
  font-size: 80%;
  letter-spacing: 0.1rem;
  font-weight: bold;
  padding: 1rem;
  transition: all 0.2s;
}
</style>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      loginAlert: false,
    };
  },
  computed: {
    isConnected() {
      return !!this.$store.state.user.token;
    },
  },
  methods: {
    async onSubmit(ev) {
      ev.preventDefault();
      this.loginAlert = false;
      let response = await this.$store.dispatch("login", this.form);
      if (response) {
        this.$router.push("/");
      } else {
        this.loginAlert = true;
      }
    },
  },
  mounted() {
    if (this.isConnected) {
      this.$router.push("/");
    }
  },
};
</script>
