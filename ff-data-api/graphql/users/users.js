const graphql = require("graphql");
const sqlite3 = require('sqlite3').verbose();

const database = new sqlite3.Database(".././ffDB.db");

const UserType = new graphql.GraphQLObjectType({
  name: "Users",
  fields: {
    user_id: { type: graphql.GraphQLID },
    username: { type: graphql.GraphQLString }
  }
});

// create a graphql query to select all and by id
var queryType = new graphql.GraphQLObjectType({
  name: 'Query',
  fields: {
    //first query to select all
    Users: {
      type: graphql.GraphQLList(UserType),
      resolve: (root, args, context, info) => {
        return new Promise((resolve, reject) => {
          // raw SQLite query to select from table
          database.all("SELECT * FROM Users;", function (err, rows) {
            if (err) {
              reject([]);
            }
            resolve(rows);
          });
        });
      }
    },
  }
});

//define schema with post object, queries, and mustation 
const schema = new graphql.GraphQLSchema({
  query: queryType
});

//export schema to use on index.js
module.exports = {
  schema
}