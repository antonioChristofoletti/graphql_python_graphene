from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_playground_handler


from app.db.database import prepare_database
from app.qql.queries import Query
from app.qql.mutations import Mutation


schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()


@app.on_event("startup")
def start_up():
    prepare_database()


app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_playground_handler()))
