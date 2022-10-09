from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book (db.Model):
    id: db.Column(db.Integer, primary_key=True)
    title: db.Column(db.String)

    created_at: db.Column(db.DateTime, server_default=db.func.now())
    updated_at: db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")