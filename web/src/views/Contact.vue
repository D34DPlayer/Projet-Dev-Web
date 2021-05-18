<template>
  <b-container>
    <h1>UN CONTACT À LA BOUCHERIE</h1>
    <p class="sous-titre">suffit pour être bien servi</p>
    <p>
      Vous ne jurez que par des produits de qualité pour garantir une
      alimentation saine et généreuse ? Nous offrons le meilleur de la nature,
      préparé dans les règles de l’art pour satisfaire tous les goûts et
      appétits. Viande de bœuf issue d’élevage de proximité, porc Duroc d’Olives
      à la chair tendre et savoureuse, charcuterie maison, fromages, sandwiches,
      plats traiteur … Voilà de quoi régaler les petits et les grands. Vous
      désirez en savoir plus ? Prenez vite
      <em>contact avec notre boucherie de Leuze (Namur).</em>
    </p>

    <p>
      Nous vous y accueillons du lundi au samedi de 8h30 à 18h30 ainsi que le
      dimanche de 8h30 à 12h. Jour de fermeture hebdomadaire : le mardi. Nous
      sommes situés non loin d’Eghezée, Bolinne, Fernelmont, La Bruyère et
      Émines. Vous pouvez nous joindre au <em>081 40 06 16</em> ou au
      <em>0477 86 07 92</em>. Un formulaire de contact est également mis à votre
      disposition sur notre site.
    </p>

    <ContactForm />
  </b-container>
</template>

<script>
import ContactForm from "@/components/ContactForm.vue";

export default {
  name: "Contact",
  components: { ContactForm },
  metaInfo: {
    title: "Nous contacter",
    meta: [
      {
        vmid: "title",
        name: "og:title",
        content: "Nous contacter",
      },
    ],
  },
};
</script>

<style scoped lang="scss">
h1 {
  color: var(--primary);
  text-align: center;
  font-weight: 200;
}

p.sous-titre {
  text-align: center;
  font-weight: 100;
  font-size: 1.5rem;
  letter-spacing: 0.3rem;
}

h2 {
  font-weight: 300;
  font-size: 1.5rem;
}

em {
  font-style: normal;
  font-weight: 400;
}

p {
  font-weight: 300;
  letter-spacing: 0.2rem;
  line-height: 1.5rem;
}
</style>
