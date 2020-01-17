const graphql = require("graphql");
const sqlite3 = require('sqlite3').verbose();

const database = new sqlite3.Database(".././ffDB.db");

const LeagueType = new graphql.GraphQLObjectType({
  name: "Leagues",
  fields: {
    league_id: { type: graphql.GraphQLID },
    league_name: { type: graphql.GraphQLString },
    total_rosters: { type: graphql.GraphQLInt },
    platform: { type: graphql.GraphQLString },
    season: { type: graphql.GraphQLInt },
    season_type: { type: graphql.GraphQLString },
    QB: { type: graphql.GraphQLInt },
    RB: { type: graphql.GraphQLInt },
    WR: { type: graphql.GraphQLInt },
    TE: { type: graphql.GraphQLInt },
    FLEX: { type: graphql.GraphQLInt },
    SUPER_FLEX: { type: graphql.GraphQLInt },
    DEF: { type: graphql.GraphQLInt },
    K: { type: graphql.GraphQLInt },
    BN: { type: graphql.GraphQLInt },
    REC_FLEX: { type: graphql.GraphQLInt },
    DL: { type: graphql.GraphQLInt },
    WRRB_FLEX: { type: graphql.GraphQLInt },
    DB: { type: graphql.GraphQLInt },
    LB: { type: graphql.GraphQLInt },
    IDP_FLEX: { type: graphql.GraphQLInt },
  }
});

// create a graphql query to select all and by id
var queryType = new graphql.GraphQLObjectType({
  name: 'Query',
  fields: {
    //first query to select all
    Leagues: {
      type: graphql.GraphQLList(LeagueType),
      resolve: (root, args, context, info) => {
        return new Promise((resolve, reject) => {
          // raw SQLite query to select from table
          database.all("SELECT * FROM Leagues;", function (err, rows) {
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