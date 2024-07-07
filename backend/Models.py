
from Config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy(Config.app)

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    idusuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contrasenia = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    monto = db.Column(db.Numeric, default=0)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.idusuario)



class Productos(db.Model):
    __tablename__ = 'productos'

    idproducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipoproducto = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric, default=0)
    stock = db.Column(db.Numeric, default=0)
    imagen_url = db.Column(db.String(255)) 
