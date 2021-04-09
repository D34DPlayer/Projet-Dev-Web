<template>
  <b-container>
    <h1>BOUCHERIE VANGEEBERGEN</h1>
    <p class="sous-titre">votre boucherie artisanale à Leuze (Namur)</p>
  <b-row><b-col sm="12" md="5" order-md="2">
    <b-embed type="video" controls>
      <source src="https://video.proxi.tools/videoentreprise/bezoom/70019596/70019596_30s-SIGNAGE_1_574.mp4" type="video/mp4">
    </b-embed>
  </b-col>
  <b-col>
    <p>Bienvenue à la Boucherie Vangeebergen, notre <em>boucherie artisanale à Leuze (Namur).</em> Avec Emilie, Michael,
      boucher
      depuis plus de 21 ans, vous y accueille dans une ambiance conviviale. Nous vous proposons un large assortiment de
      viandes de premier choix, savoureuses et saines. Vous y trouverez également des charcuteries et des fromages ainsi
      qu’une variété de plats maison, dont la carte varie toutes les semaines.</p>
  </b-col></b-row>
    <h2>Des viandes de qualité</h2>
    <p>Pour vous servir une <em>viande d’excellence</em>, nous privilégions un partenariat avec les fermes de la région
      en qui nous
      avons toute confiance. La viande de porc est quant à elle issue de la race Duroc d’Olives, caractérisée par un
      pelage roux et les oreilles tombantes. Leur alimentation, à base de céréales pures et d’huile d’olive, garantit
      une
      viande plus tendre et savoureuse. Nous proposons également du veau, de l’agneau et de la volaille. En saison, le
      gibier est mis à l’honneur, tandis qu’une viande étrangère occupe les étals de la boucherie une fois par semaine.
    </p>

    <h2>Des charcuteries et des fromages variés</h2>
    <p>Au rayon charcuterie, nous proposons une grande variété de <em>produits préparés maison</em>, dans les règles
      d’hygiène les
      plus strictes. Nous avons des saucisses sèches, des cervelas, divers boudins blancs, le pâté du chef, du rosbif,
      etc. Le jambon, salami (à l’ail et sans ail), le saucisson de jambon … font partie de notre assortiment de
      charcuterie traditionnelle. Pour les amateurs de fromage, nous nous fournissons dans une ferme locale.</p>

    <h2>Le service traiteur</h2>
    <p>Chaque semaine, nous sélectionnons les meilleurs produits pour préparer des plats traiteur ainsi que d’autres
      suggestions à réchauffer chez vous. Nous nous adaptons à la demande de nos clients pour satisfaire tous les goûts.
      Nos <em>sandwiches frais</em> du jour vous régaleront lors d’un déjeuner convivial. Pour être servi dans les
      meilleures
      conditions, il est préférable de passer commande. Dans tous les cas, la sécurité alimentaire est toujours
      respectée
      au sein de notre boucherie artisanale.</p>

    <h2>Contactez la Boucherie Vangeebergen</h2>
    <p>Prenez vite contact avec la boucherie pour passer votre commande ou réserver votre colis de viande. Nous sommes
      ouverts du lundi au dimanche à l’exception du mardi. Notre établissement est situé à Leuze (Namur), dans les
      environs d’Éghezée, Bolinne, Fernelmont, La Bruyère et Émines.</p>
  </b-container>
</template>

<script>
export default {
  name: "Accueil",
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
  letter-spacing: .3rem;
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
  letter-spacing: .2rem;
  line-height: 1.5rem;
}
</style>