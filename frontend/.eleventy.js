// eleventy.config.js
const sqlitePlugin = require('./_plugins/sqlconnect.js');
module.exports = function(eleventyConfig) {
    // Load the SQLite plugin and pass options, such as the database path

    eleventyConfig.addPassthroughCopy("-/");

    eleventyConfig.addPlugin(sqlitePlugin, {
        dbPath: '../data/db.sqlite' // Adjust the path to your SQLite database as needed
    });

    eleventyConfig.addCollection("experiments", function(collectionApi) {
        return collectionApi.getFilteredByGlob("experiments/*.md").filter(item => item.fileSlug !== "index");
    });


    // set _site path
    // Check if we're in production or development
    let isDev = process.env.ELEVENTY_DEV_MODE === "Y";

    // Set up different siteBase URLs for GitHub Pages and local development
    let repoName = "/this-social-media-site-does-not-exist"; // GitHub repo name
    let baseUrl = isDev ? "" : `${repoName}`;

    // Pass this as global data
    eleventyConfig.addGlobalData("baseUrl", baseUrl);

    return {
        dir: {
            input: "./", // your source directory
            output: isDev ? "_site_dev" : "_site" // Output directory
        }
    };
};