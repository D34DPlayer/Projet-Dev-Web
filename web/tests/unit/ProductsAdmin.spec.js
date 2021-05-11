import { mount, createLocalVue } from "@vue/test-utils";
import ProductsAdmin from "@/components/ProductsAdmin.vue";

import { BootstrapVue } from "bootstrap-vue";

const localVue = createLocalVue();

localVue.use(BootstrapVue);

const elem = document.createElement("div");
if (document.body) {
  document.body.appendChild(elem);
}

if (document.body) {
  document.body.appendChild(elem);
}

const products = [
  {
    id: 4,
    name: "Bananne",
    categorie: "Fruit",
    description: "c'est un fruit",
    photos: [
      "https://www.boucherie-vangeebergen.be/media/images/gallery/10/big/11.jpg",
    ],
    price: 50.0,
    promo_price: 25.0,
    price_type: "/kilo",
    visibility: true,
  },
  {
    id: 5,
    name: "Tomate",
    categorie: "Légume",
    description: "c'est pas un fruit",
    photos: [
      "https://www.boucherie-vangeebergen.be/media/images/gallery/10/big/12.jpg",
    ],
    price: 45.0,
    promo_price: null,
    price_type: "/unité",
    visibility: false,
  },
];
const wrapper = mount(ProductsAdmin, {
  localVue,
  attachTo: elem,
  propsData: { products },
});

describe("ProductsAdmin.vue", () => {
  const rows = wrapper.findAll("tbody tr");
  it("renders two rows", () => {
    expect(rows.length).toBe(2);
  });

  const firstRow = rows.wrappers[0];
  const secondRow = rows.wrappers[1];

  it("renders the name correctly", () => {
    expect(firstRow.find('td[aria-colindex="1"]').text()).toMatch(
      products[0].name
    );
  });

  it("renders the category correctly", () => {
    expect(firstRow.find('td[aria-colindex="2"]').text()).toMatch(
      products[0].categorie
    );
  });

  it("hides the description by default", () => {
    expect(firstRow.text()).not.toMatch(products[0].description);
  });

  it("shows details on button click", async () => {
    firstRow.find('td[aria-colindex="7"] button').trigger("click");
    await localVue.nextTick();
    expect(wrapper.find(".b-table-details").exists()).toBe(true);
  });

  it("shows the description on detail", () => {
    expect(wrapper.find(".b-table-details").text()).toMatch(
      products[0].description
    );
  });

  it("shows the photo(s) on detail", () => {
    expect(wrapper.findAll(".b-table-details .images-item").length).toBe(1);
    expect(
      wrapper
        .findAll(".b-table-details .images-item img")
        .wrappers[0].attributes().src
    ).toMatch(products[0].photos[0]);
  });

  it("renders the price correctly", () => {
    expect(firstRow.find('td[aria-colindex="3"]').text()).toMatch("50.00€");
  });

  it("renders the promo price correctly", () => {
    expect(firstRow.find('td[aria-colindex="4"]').text()).toMatch("25.00€");
    expect(secondRow.find('td[aria-colindex="4"]').text()).toMatch("-----");
  });

  it("renders the price type correctly", () => {
    expect(firstRow.find('td[aria-colindex="5"]').text()).toMatch("/kilo");
  });

  it("renders the visibility correctly", () => {
    expect(firstRow.find('td[aria-colindex="6"] input').element.checked).toBe(
      true
    );
    expect(secondRow.find('td[aria-colindex="6"] input').element.checked).toBe(
      false
    );
  });
});
