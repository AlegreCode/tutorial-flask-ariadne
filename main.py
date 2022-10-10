import os
from ariadne import QueryType, gql, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from ariadne import ScalarType
from flask import Flask, request, jsonify
from datetime import datetime

from models import db, ma, book, author, authorSchema

type_defs = gql("""
    scalar Datetime

    type Author {
        id: ID
        name: String
        lastname: String
        books: [Book]
        created_at: Datetime
        updated_at: Datetime
    }

    type Book {
        id: ID
        title: String
        author: Author!
        created_at: Datetime
        updated_at: Datetime
    }

    type Query {
        author(id: ID!): Author!
        authors: [Author]
        book(id: ID!): Book!
        books: [Book]
    }

    type Mutation {
        author(name: String!, lastname: String!): Author!
        book(title: String!): Book!
    }
""")

authors_schema = authorSchema.AuthorSchema(many=True)

query = QueryType()


@query.field("authors")
def resolve_authors(_, info):
    data = author.Author.query.all()
    return authors_schema.dump(data)

datetime_scalar = ScalarType("Datetime")
@datetime_scalar.serializer
def datetime_serializer(value):
    return datetime.strptime(value,"%Y-%m-%dT%H:%M:%S")

schema = make_executable_schema(type_defs, query, datetime_scalar)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}@{}:{}/{}".format(os.environ.get("USER"), os.environ.get("HOST"), os.environ.get("PORT"), os.environ.get("DATABASE"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)