const path = require("path");
const PrerenderSpaPlugin = require("prerender-spa-plugin");

const productionPlugins = [
  new PrerenderSpaPlugin({
    staticDir: path.join(__dirname, "dist"),
    routes: ["/", "/about", "/contact"],
    renderer: new PrerenderSpaPlugin.PuppeteerRenderer({
      inject: {
        foo: "bar",
      },
      headless: true,
      renderAfterDocumentEvent: "render-event",
    }),
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
