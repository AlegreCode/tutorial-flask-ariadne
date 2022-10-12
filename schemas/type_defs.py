from ariadne import gql, ScalarType
from datetime import datetime

datetime_scalar = ScalarType("Datetime")
@datetime_scalar.serializer
def datetime_serializer(value):
    return datetime.strptime(value,"%Y-%m-%dT%H:%M:%S")

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
        addAuthor(name: String!, lastname: String!): Author!
        addBook(title: String!, author_id: ID): Book!

        updateAuthor(id: ID!, name: String!, lastname: String!): Author!
        updateBook(id: ID!, title: String!): Book!

        deleteAuthor(id: ID!): Author!
        deleteBook(id: ID!): Book!
    }
""")