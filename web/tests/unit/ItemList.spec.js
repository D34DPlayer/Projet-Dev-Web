import { mount, RouterLinkStub } from "@vue/test-utils";
import Vuex from "vuex";
import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import VueRouter from "vue-router";
import ItemList from "@/components/ItemList";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(Vuex);
Vue.use(VueRouter);

const component = () => {
  return mount(ItemList, {
    propsData: {
      product: {
        id: 4,
        name: "Banane",
        categorie: "Fruit",
        description: "c'est un fruit",
        photos: ["/images/products/4/alpaga.jpg"],
        price: 50.0,
        promo_price: 25.0,
        price_type: "/kilo",
        visibility: true,
      },
    },
    stubs: { RouterLink: RouterLinkStub },
  });
};

describe("ItemList.spec.js", () => {
  it("Test text de la carte.", () => {
    const wrapper = component();
    expect(wrapper.text()).toMatch("Banane");
    expect(wrapper.text()).toMatch("Fruit");
    expect(wrapper.text()).toMatch("25.00€");
  });

  it("Test de click sur une carte", async () => {
    const wrapper = component();
    await wrapper.trigger("click");
    await Vue.nextTick();
    expect(wrapper.findComponent(RouterLinkStub).props().to).toBe(
      "/products/4"
    );
  });

  it("Test Photo Source Image", () => {
    const wrapper = component();
    expect(wrapper.vm.imageFound.backgroundImage).toBe(
      "url(/images/products/4/alpaga.jpg)"
    );
  });

  it("Test No Photo Source Image", () => {
    const wrapper = mount(ItemList, {
      propsData: {
        product: {
          id: 4,
          name: "Banane",
          categorie: "Fruit",
          description: "c'est un fruit",
          photos: [],
          price: 50.0,
          promo_price: 25.0,
          price_type: "/kilo",
          visibility: true,
        },
      },
      stubs: { RouterLink: RouterLinkStub },
    });
    expect(wrapper.vm.imageFound).isEmpty;
  });
});
