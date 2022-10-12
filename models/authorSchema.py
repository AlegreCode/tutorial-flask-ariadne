from models import ma, author

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = author.Author
        include_relationships = True
    books= ma.List(ma.Nested("BookSchema", exclude=("author",)))