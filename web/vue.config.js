const path = require("path");
const fs = require("fs");

const PrerenderSpaPlugin = require("prerender-spa-plugin");
const SitemapPlugin = require("sitemap-webpack-plugin").default;
const RobotstxtPlugin = require("robotstxt-webpack-plugin");

const routerPaths = ["/", "/about", "/login", "/products", "/contact"];

const productionPlugins = [
  new PrerenderSpaPlugin({
    staticDir: path.join(__dirname, "dist"),
    routes: routerPaths,
    renderer: new PrerenderSpaPlugin.PuppeteerRenderer({
      inject: {
        foo: "bar",
      },
      headless: true,
      renderAfterDocumentEvent: "render-event",
    }),
  }),
  new SitemapPlugin({
    base: `https://${process.env.DOMAIN_NAME}`,
    paths: routerPaths,
    options: {
      fileName: "sitemap.xml",
      lastMod: true,
      changeFreq: "daily",
    },
  }),
  new RobotstxtPlugin({
    sitemap: `https://${process.env.DOMAIN_NAME}/robots.txt`,
    host: `https://${process.env.DOMAIN_NAME}`,
  }),
];

module.exports = {
  devServer: {
    watchOptions: {
      poll: 1000,
    },
  },
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === "production") {
      config.plugins.push(...productionPlugins);
    }
  },
};
