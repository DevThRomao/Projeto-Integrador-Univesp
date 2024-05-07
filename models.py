from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Voluntario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)  
    endereço = db.Column(db.String(200), nullable=False)  
