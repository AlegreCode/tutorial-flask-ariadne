import imp
import os
from ariadne import QueryType, MutationType,graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

from models import db, ma
from models.author import Author
from models.book import Book
from models.authorSchema import AuthorSchema
from models.bookSchema import BookSchema
from schemas.type_defs import type_defs, datetime_scalar


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

query = QueryType()
mutation = MutationType()


@query.field("authors")
def resolve_authors(_, info):
    data = Author.query.all()
    return authors_schema.dump(data)

@query.field("author")
def resolve_author(_, info, id):
    data = Author.query.get(id)
    return author_schema.dump(data)

@query.field("books")
def resolve_books(_, info):
    data = Book.query.all()
    return books_schema.dump(data)

@query.field("book")
def resolve_book(_, info, id):
    data = Book.query.get(id)
    return book_schema.dump(data)

@mutation.field("addAuthor")
def resolve_add_author(_, info, name, lastname):
    author = Author(name=name, lastname=lastname)
    db.session.add(author)
    db.session.commit()
    return author_schema.dump(author)

@mutation.field("addBook")
def resolve_add_book(_, info, title, author_id):
    book = Book(title=title, author_id=author_id)
    db.session.add(book)
    db.session.commit()
    return book_schema.dump(book)

@mutation.field("updateAuthor")
def resolve_update_author(_, info, id, name, lastname):
    author = Author.query.get(id)
    author.name = name
    author.lastname = lastname
    db.session.commit()
    return author_schema.dump(author)

@mutation.field("updateBook")
def resolve_update_book(_, info, id, title):
    book = Book.query.get(id)
    book.title = title
    db.session.commit()
    return book_schema.dump(book)

@mutation.field("deleteAuthor")
def resolve_delete_author(_, info,  id):
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()
    return author_schema.dump(author)

@mutation.field("deleteBook")
def resolve_delete_book(_, info, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return book_schema.dump(book)

schema = make_executable_schema(type_defs, [query, mutation, datetime_scalar])

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