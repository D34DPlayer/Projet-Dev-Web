import { mount } from "@vue/test-utils";
import ProductForm from "@/components/ProductForm.vue";
import Vuex from "vuex";
import Vue from "vue";
import VueRouter from "vue-router";
import {
    BFormSelect,
    BButton,
    BootstrapVue,
    BootstrapVueIcons
} from "bootstrap-vue";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(Vuex);
Vue.use(VueRouter);

describe("ProductForm.vue", () => {
    const wrapper = mount(ProductForm, {
        store,
        propsData: {
            static: true
        }
    });

    it("", async () => {
        wrapper.findComponent(BButton).trigger("click");
        await Vue.nextTick();

        expect(wrapper.find("#input-name").vm.validity.valueMissing).toBeTruthy();
        expect(wrapper.find("#input-categorie").vm.validity.valueMissing).toBeTruthy();
        expect(wrapper.find("#textarea-desc").vm.validity.valueMissing).toBeTruthy();
        expect(wrapper.find("#input-prix").vm.validity.valueMissing).toBeTruthy();

        wrapper.setData({
            form: {
                name: "boudin noir",
                categorie: "boudin",
                description: "très bon",
                price: 25
            }
        });
        await Vue.nextTick();

        expect(wrapper.find("#input-name").vm.checkValidity()).toBeTruthy();
        expect(wrapper.find("#input-categorie").vm.checkValidity()).toBeTruthy();
        expect(wrapper.find("#textarea-desc").vm.checkValidity()).toBeTruthy();
    });
});
