from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true

db = SQLAlchemy()

class Author (db.Model):
    id: db.Column(db.Integer, primary_key=True)
    name: db.Column(db.String(255))
    lastname: db.Column(db.String(255))
    
    created_at: db.Column(db.DateTime, server_default=db.func.now())
    updated_at: db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())