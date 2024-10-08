// eleventy.config.js
const sqlitePlugin = require('./_plugins/sqlconnect.js');
console.log('start')
module.exports = function(eleventyConfig) {
    // Load the SQLite plugin and pass options, such as the database path

    eleventyConfig.addPassthroughCopy("-/");

    eleventyConfig.addPlugin(sqlitePlugin, {
        dbPath: '../data/db.sqlite' // Adjust the path to your SQLite database as needed
    });

  eleventyConfig.addCollection("experiments", function(collectionApi) {
    return collectionApi.getFilteredByGlob("experiments/*.md").filter(item => item.fileSlug !== "index");
  });


    return {
        dir: {
            input: "./", // your source directory
            output: "_site" // your output directory
        }
    };
};