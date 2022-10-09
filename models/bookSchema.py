from models import ma, book

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = book
        include_fk = True

