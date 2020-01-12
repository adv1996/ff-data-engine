const graphql = require("graphql");
const sqlite3 = require('sqlite3').verbose();

const database = new sqlite3.Database(".././ffDB.db");

const UserLeagueType = new graphql.GraphQLObjectType({
  name: "UserLeague",
  fields: {
    user_id: { type: graphql.GraphQLID },
    league_id: { type: graphql.GraphQLID },
    roster_id: { type: graphql.GraphQLID },
    wins: { type: graphql.GraphQLID },
    ties: { type: graphql.GraphQLID },
    fpts: { type: graphql.GraphQLID },
    losses: { type: graphql.GraphQLID },
    fpts_against: { type: graphql.GraphQLID },
  }
});

// create a graphql query to select all and by id
var queryType = new graphql.GraphQLObjectType({
  name: 'Query',
  fields: {
    //first query to select all
    UserLeague: {
      type: graphql.GraphQLList(UserLeagueType),
      resolve: (root, args, context, info) => {
        return new Promise((resolve, reject) => {
          // raw SQLite query to select from table
          database.all("SELECT * FROM UserLeague;", function (err, rows) {
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