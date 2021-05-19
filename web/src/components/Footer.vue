<template>
  <footer>
    <b-container class="p-4 mt-3">
      <b-row align-v="center">
        <b-col sm="12" md="4" class="p-2">
          <h1>Contactez-nous</h1>
          <p class="sous-titre">Boucherie Vangeebergen</p>
          <b-row align-v="center">
            <b-col cols="2">
              <b-icon-geo-alt-fill class="openingDay" />
            </b-col>
            <b-col>
              <div>{{ contact.address.street }}</div>
              <div>{{ contact.address.city }}</div>
              <div>Plan d’accès</div>
            </b-col>
          </b-row>
          <b-row align-v="center">
            <b-col cols="2">
              <b-icon-telephone-fill class="openingDay" />
            </b-col>
            <b-col>
              <div>Tél : {{ contact.phone.office }}</div>
              <div>Gsm : {{ contact.phone.mobile }}</div>
            </b-col>
          </b-row>
          <b-row align-v="center">
            <b-col cols="2">
              <b-icon-envelope-fill class="openingDay" />
            </b-col>
            <b-col>
              <div>{{ contact.email }}</div>
              <div>N° TVA : {{ contact.tva }}</div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm="12" md="3" class="text-center p-2">
          <img class="image-logo" src="@/assets/logo.png" alt="Boucherie" />
        </b-col>
        <b-col sm="12" md="5" class="p-2">
          <h1>Heures d'ouverture</h1>
          <b-row>
            <b-col
              sm="6"
              md="12"
              xl="6"
              class="ligne-horaire"
              v-for="[key, day] in days"
              :key="key"
            >
              <span class="openingDay">{{ key }}</span>
              <span>
                {{ formatDay(day) }}
              </span>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <b-row cols="12" class="social-media">
        <b-link :href="contact.facebook" class="facebook" target="_blank">
          <b-icon-facebook />
        </b-link>
      </b-row>
    </b-container>
  </footer>
</template>

<script>
import {
  BIconGeoAltFill,
  BIconTelephoneFill,
  BIconEnvelopeFill,
  BIconFacebook,
} from "bootstrap-vue";
export default {
  name: "Footer",
  components: {
    BIconGeoAltFill,
    BIconTelephoneFill,
    BIconEnvelopeFill,
    BIconFacebook,
  },
  mounted() {
    this.$store.dispatch("horaire/getHoraire");
    this.$store.dispatch("contact/getContact");
  },
  computed: {
    days() {
      let days = this.$store.state.horaire.days;
      return Object.entries(days).filter((i) => i[1].is_open);
    },
    contact() {
      return this.$store.state.contact.contact;
    },
  },
  methods: {
    formatDay(day) {
      let open = day.open.split(":");
      let close = day.close.split(":");
      return `${open[0]}h${open[1]}-${close[0]}h${close[1]}`;
    },
  },
};
</script>

<style scoped lang="scss">
footer {
  background-color: #000;
  color: #fff;
}

@media (min-width: 992px) {
  footer {
    overflow: hidden;
    padding-top: 3.75rem;
    position: relative;

    &::before {
      content: "";
      background: #fff;
      position: absolute;
      left: 0;
      height: 100%;
      right: 0;
      top: -85%;
      z-index: 1;
      -webkit-clip-path: inset(0% -28% round 0% 0% 80% 80%);
      clip-path: inset(0% -35% round 0% 0% 80% 80%);
    }
  }
  .facebook {
    margin: 0 0 0 1.1rem !important;
  }
}

.image-logo {
  width: 66%;
}

.openingDay {
  display: inline-block;
  text-align: center;
  border: 0.1rem solid rgba(255, 255, 255, 0.13);
  border-radius: 0.25rem;
  margin: 0 0.5rem 0.5rem 0;
  padding: 0.17rem 0 0 0;
  height: 2rem;
  width: 2rem;
  &:first-letter {
    text-transform: capitalize;
  }
}

svg.openingDay {
  padding: 0.3rem;
}

.ligne-horaire {
  margin-left: auto;
  margin-right: auto;
  width: auto;
}

.social-media {
  border-top: 0.1rem solid rgba(255, 255, 255, 0.13);
  padding: 0.5rem;
}

.facebook {
  font-size: 1.5em;
  color: #fff;
  margin: auto;
  transition: color 0.4s;
  &:active {
    color: #fff;
  }
  &:visited {
    color: #fff;
  }
  &:hover {
    color: var(--primary);
  }
}
</style>
