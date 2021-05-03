import { shallowMount } from "@vue/test-utils";
import ItemList from "@/components/ItemList.vue"

describe("ItemList.test.js", () =>{
    let cmp;

    beforeEach(() => {
       cmp = shallowMount(App, {
           data: {"id":4,
               "name":"Bananne",
               "categorie":"Fruit",
               "description":"c'est un fruit",
               "photos":["/images/products/4/alpaga.jpg"],
               "price":50.0,
               "promo_price":25.0,
               "price_type":"/kilo",
               "visibility":true}
       });
    });

    it("equals name to Bananne", () => {
       expect(cmp.vm.name).toEqual("Bananne");
    });

    it("equals categorie to Fruit", () => {
       expect(cmp.vm.categorie).toEqual("Fruit");
    });
    it("has the expected html structure", () => {
        expect(cmp.element).toMatchSnapshot();
    });
});