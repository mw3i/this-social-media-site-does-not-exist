const sqlite3 = require('sqlite3').verbose();

module.exports = function(eleventyConfig, options = {}) {
  const dbPath = options.dbPath || './db.sqlite'; // Use provided dbPath or default

  // Helper function to execute SQL query
  const executeQuery = (query) => {
    return new Promise((resolve, reject) => {
      let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
        if (err) {
          console.error("Error opening the database:", err);
          reject(err);
        }
      });

      db.all(query, [], (err, rows) => {
        if (err) {
          console.error("SQL error:", err);
          reject(err);
        } else {
          resolve(rows); // Resolve with query results
        }
      });

      // Close the database
      db.close((err) => {
        if (err) {
          console.error("Error closing the database:", err);
        }
      });
    });
  };

  // Add SQL filter
  eleventyConfig.addAsyncFilter("sql", async function(query) {
    try {
      const rows = await executeQuery(query);
      return rows; // Return the rows directly as an array of objects
    } catch (error) {
      return `SQL error: ${error.message}`; // Return error message as string
    }
  });
};
