from models import ma, book

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = book.Book
        include_fk = True

