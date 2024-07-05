
from Config import Config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(Config.app)

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    idusuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contrasenia = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    monto = db.Column(db.Numeric, default=0)



class Productos(db.Model):
    __tablename__ = 'productos'

    idproducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipoproducto = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric, default=0)
    stock = db.Column(db.Numeric, default=0)
