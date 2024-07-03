from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/Tp1-Intro'
db = SQLAlchemy(app)


class Usuarios(db.Model):
    __tablename__ = 'Usuarios'

    idUsuarios = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contrasenia = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    monto = db.Column(db.Numeric, default=0)
    socio = db.Column(db.Boolean, default=False)
    idCarrito = db.Column(db.Integer, default=None)