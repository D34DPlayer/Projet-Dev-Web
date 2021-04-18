<template>
  <b-carousel id="carousel-1" :interval="5000" controls class="carousel">
    <b-carousel-slide
      img-src="https://www.boucherie-vangeebergen.be/media/images/gallery/10/big/11.jpg"
    ></b-carousel-slide>
    <b-carousel-slide
      img-src="https://www.boucherie-vangeebergen.be/media/images/gallery/10/big/12.jpg"
    ></b-carousel-slide>
  </b-carousel>
</template>

<style scoped lang="scss">
@media (min-width: 992px) {
  .carousel {
    overflow: hidden;

    &::before {
      content: "";
      background: #fff;
      position: absolute;
      left: 0;
      height: 100%;
      right: 0;
      bottom: -87.4%;
      z-index: 1;
      webkit-clip-path: inset(0% -52% round 100% 100% 0 0%);
      clip-path: inset(0% -52% round 100% 100% 0 0%);
    }
  }
}
</style>

<script>
export default {
  name: "Carousel",
};
</script>
