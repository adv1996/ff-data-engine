const  express  =  require('express');
const ExpressGraphQL = require("express-graphql");
const userSchema = require("./graphql/users/users.js");
const userLeagueSchema = require("./graphql/userLeague/userLeague.js");
const  app  =  express();
const cors = require('cors')

const {mergeSchemas} = require('graphql-tools');
const schema = mergeSchemas({
    schemas: [userSchema.schema, userLeagueSchema.schema]
})
app.use(cors())
app.use("/graphql", ExpressGraphQL({ schema: schema, graphiql: true}));

app.listen(4000, () => {
    console.log("GraphQL server running at http://localhost:4000");
});