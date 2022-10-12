from models import db

class Author (db.Model):
    __tablename__= "authors"
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    lastname= db.Column(db.String(255))

    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at= db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())