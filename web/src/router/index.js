import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/login",
    name: "Se connecter",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/Login.vue"),
  },
  {
    path: "/products",
    name: "Produits",
    component: () =>
      import(/* webpackChunkName: "products" */ "../views/Products.vue"),
  },
  {
    path: "/products/:id",
    name: "Détail Produit",
    component: () =>
        import(/* webpackChunkName: "detail" */ "../views/Detail.vue")
  },
  {
    path: "/contact",
    name: "Contact",
    component: () =>
      import(/* webpackChunkName: "contact" */ "../views/Contact.vue"),
  },
  {
    path: "/admin",
    name: "Administration",
    component: () =>
      import(/* webpackChunkName: "admin" */ "../views/Admin.vue"),
  },
  {
    path: "/comments",
    name: "Commentaires",
    component: () =>
      import(/* webpackChunkName: "admin" */ "../views/Comments.vue"),
  },
  {
    path: "/logout",
    name: "Se deconnecter",
    component: () =>
      import(/* webpackChunkName: "logout" */ "../views/Logout.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
