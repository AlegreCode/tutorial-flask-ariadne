from models import db

class Book (db.Model):
    __tablename__="books"
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(255))

    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at= db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))