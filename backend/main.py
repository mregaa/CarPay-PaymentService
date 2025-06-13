from fastapi import FastAPI
from ariadne import gql, QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
from database import init_db
from resolvers import (
    resolve_get_payment_by_id,
    resolve_get_payment_status,
    resolve_create_payment,
    resolve_get_payments_by_user,
    resolve_update_payment_status,
    resolve_delete_payment,
    get_all_payments
)

type_defs = gql(open("schema.graphql").read())

query = QueryType()
mutation = MutationType()

query.set_field("getPaymentById", resolve_get_payment_by_id)
query.set_field("getPaymentStatus", resolve_get_payment_status)
query.set_field("getPaymentsByUser", resolve_get_payments_by_user)
query.set_field("getAllPayments", get_all_payments)
mutation.set_field("updatePaymentStatus", resolve_update_payment_status)
mutation.set_field("createPayment", resolve_create_payment)
mutation.set_field("deletePayment", resolve_delete_payment)


schema = make_executable_schema(type_defs, [query, mutation])

app = FastAPI()
app.mount("/graphql", GraphQL(schema, debug=True))


@app.on_event("startup")
async def startup_event():
    init_db()
    print("API siap! Akses GraphiQL di http://localhost:8000/graphql")

@app.get("/")
async def root():
    return {"message": "Selamat datang di Star Wars GraphQL API! Buka /graphql untuk mulai."}
