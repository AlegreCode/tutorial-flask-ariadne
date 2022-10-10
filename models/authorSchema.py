from models import ma, author

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = author.Author