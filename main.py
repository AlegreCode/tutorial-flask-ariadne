import os
from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

from models import db, ma, book, author, authorSchema, bookSchema
from schemas.type_defs import type_defs, datetime_scalar


author_schema = authorSchema.AuthorSchema()
authors_schema = authorSchema.AuthorSchema(many=True)

book_schema = bookSchema.BookSchema()
books_schema = bookSchema.BookSchema(many=True)

query = QueryType()


@query.field("authors")
def resolve_authors(_, info):
    data = author.Author.query.all()
    return authors_schema.dump(data)

@query.field("author")
def resolve_author(_, info, id):
    data = author.Author.query.get(id)
    return author_schema.dump(data)

@query.field("books")
def resolve_books(_, info):
    data = book.Book.query.all()
    return books_schema.dump(data)

@query.field("book")
def resolve_book(_, info, id):
    data = book.Book.query.get(id)
    return book_schema.dump(data)


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
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

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