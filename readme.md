# Graphql

Powerful, open-source data query language for APIs
Developed by Meta in 2012, publicly released in 2015.

# Components

## Mutation

Component used to make changes in the server, such as, create, update and delete.

## Query

Component used to make searches in the server

# Object Types

Component used to structure how the data will be structured, with fields and resolvers (functions that define how certain fields will be retrieved)

## Graphql vs RESTful API

1. Efficient data loading
2. Strong typing
    -> Self-documentaing APIs
    -> Auto-completion
3. Managing change
    -> Adding or deprecating fields is smoother


## Making search

Query example:

query your_query_name($season: String, $limit: Int, $skip: Int, $noWeight: Boolean!, $include_player_height: Boolean!) {
  players(season: $season, limit: $limit, skip: $skip) {
    ...basic_player_info
    draftYear
    draftRound
  }
}

fragment basic_player_info on Player {
  playerName
  playerHeight @include(if: $include_player_height)
  playerWeight @skip(if: $noWeight)
  teamAbbreviation
}

Variable example:

{
  "season": "2018-19",
  "limit": 20,
  "skip": 5,
  "noWeight": true,
  "include_player_height": false
}


It is possible define which fields will be retrieved, pagination (limit, skip).

It is possible define variables to be used during the search, which can be mandatory or not.

Fragment serves to create small search query that can be included in others queries.


# Design Decisions: Code first or Schema First

Schema-first

We start by writing up the schema in the GraphQL SDL

Pro: Clear data contract, collaborative

Top schema-first libraries in python ariadne, tartaflette

Code-first

Write the app, get the schema as a byproduct

Pro: Always consistent, easier to define more complex relationships

Top code-first libraries in python: graphene, strawberry

How do we choose?

Who's doing the dev? Are they stronger in python or GDL?

How big is the project and how many teams are collaborating?

Architect preferences and other considerations


# Scaling up the graphql server

Using federation, it is possible to handle large and complex API logic. The idea is that the graph server will be split into multiple small GraphQL servers (microservices), and there will be a main GraphQL server (gateway) to handle requests and forward them to the appropriate microservice.