<template>
  <footer>
    <b-container class="p-4 mt-3">
      <b-row align-v="center">
        <b-col sm="12" md="4" class="p-2">
          <h1>Contactez-nous</h1>
          <p class="sous-titre">Boucherie Vangeebergen</p>
          <b-container>
            <b-row align-v="center">
              <b-col cols="2">
                <b-icon-geo-alt-fill class="openingDay" />
              </b-col>
              <b-col>
                <div>Chaussée de Namur 301</div>
                <div>B-5310 Leuze (Nam.)</div>
                <div>Plan d’accès</div>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col cols="2">
                <b-icon-telephone-fill class="openingDay" />
              </b-col>
              <b-col>
                <div>Tél : 081 40 06 16</div>
                <div>Gsm: 0477 86 07 92</div>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col cols="2">
                <b-icon-envelope-fill class="openingDay" />
              </b-col>
              <b-col>
                <div>info@boucherie-vangeebergen.be</div>
                <div>N° TVA : BE 0700.234.189</div>
              </b-col>
            </b-row>
          </b-container>
        </b-col>
        <b-col sm="12" md="4" class="text-center p-2">
          <img class="image-logo" src="@/assets/logo.png" alt="Boucherie" />
        </b-col>
        <b-col sm="12" md="4" class="p-2">
          <h1>Heures d'ouverture</h1>
          <b-container>
            <b-row>
              <b-col sm="6" md="12" xl="6" order-xl="1" class="ligne-horaire">
                <span class="openingDay">Lu</span>
                <span>8h30-18h30</span>
              </b-col>
              <b-col sm="6" md="12" xl="6" order-xl="3" class="ligne-horaire">
                <span class="openingDay">Me</span>
                <span>8h30-18h30</span>
              </b-col>
              <b-col sm="6" md="12" xl="6" order-xl="5" class="ligne-horaire">
                <span class="openingDay">Je</span>
                <span>8h30-18h30</span>
              </b-col>
              <b-col sm="6" md="12" xl="6" order-xl="2" class="ligne-horaire">
                <span class="openingDay">Ve</span>
                <span>8h30-18h30</span>
              </b-col>
              <b-col sm="6" md="12" xl="6" order-xl="4" class="ligne-horaire">
                <span class="openingDay">Sa</span>
                <span>8h30-18h30</span>
              </b-col>
              <b-col sm="6" md="12" xl="6" order-xl="6" class="ligne-horaire">
                <span class="openingDay">Di</span>
                <span>8h30-18h30</span>
              </b-col>
            </b-row>
          </b-container>
        </b-col>
      </b-row>
      <b-row cols="12" class="social-media">
        <b-link
          href="https://www.facebook.com/boucherievangeebergen/"
          class="facebook"
          target="_blank"
        >
          <b-icon-facebook />
        </b-link>
      </b-row>
    </b-container>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped lang="scss">
footer {
  background-color: #000;
  color: #fff;
}

@media (min-width: 768px) {
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
