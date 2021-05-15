<template>
  <b-container>
    <b-carousel
        id="carousel-1"
        ref="carouselDetail"
        v-model="slide"
        :interval="1500"
        indocators
        hover-pause
        background="black"
        style="text-shadow: 1px 1px 2px #333;"
        img-height="2rem"
        img-width="2rem"
        @sliding-start="onSlideStart"
        @sliding-end="onSlideEnd"
    >
        <b-carousel-slide
            v-for="(image, index) in images"
            :key="index"
            :img-src="image"
            :img-alt="`${name}:${index}`"
        >
        </b-carousel-slide>
    </b-carousel>
  </b-container>
</template>

<script>
export default {
  name: "CarrouselDetail",
  props: ["images", "name"],
  data() {
    return {
      slide: 0,
      sliding: null,
    }
  },
  methods: {
    onSlideStart(numSlide) {
      this.slide = numSlide;
      this.sliding = true;
    },
    onSlideEnd(numSlide) {
      this.slide = numSlide;
      this.sliding = false;
    },
    prev() {
      this.$refs.carouselDetail.prev();
    },
    next() {
      this.$refs.carouselDetail.next();
    },
  }
}

</script>

<style scoped>

</style>

