from flask import Flask, jsonify, request, url_for, redirect, session, render_template
#from Config import Config
#from Models import Usuarios, Productos, db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

app = Flask(__name__, template_folder='frontend')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/tp1_intro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ajdhaskjdhasdkashdj'

db = SQLAlchemy(app)

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    idusuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contrasenia = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    monto = db.Column(db.Numeric, default=0)



@app.route('/login', methods=['POST'])
def inicio_sesion():
    datos_login = request.get_json()
    email = datos_login.get('email')
    password = datos_login.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan datos de inicio de sesión'}), 400

    usuario = Usuarios.query.filter_by(email=email, contrasenia=password).first()
    if usuario:
        return jsonify({'mensaje': 'Inicio de sesión exitoso', 'idusuario': usuario.idusuario}), 200
    else:
        return jsonify({'error': 'Correo o contraseña incorrectos'}), 401
    

@app.route('/logout')
def cerrar_sesion():
    logout_user()
    return redirect(url_for('login'))


@app.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Productos.query.all()
    productos_serializados = []
    for producto in productos:
        producto_serializados = {
            'id' : producto.idproducto,
            'nombre': producto.nombre,
            'tipo': producto.tipoproducto,
            'precio': producto.precio,
            'stock': producto.stock
        }
        productos_serializados.append(producto_serializados)
        
    return jsonify(productos_serializados), 200


@app.route('/productos/<int:idproducto>', methods=['PUT'])
def actualizar_producto(idproducto):
    producto_actualizado = request.get_json()
    if not producto_actualizado:
        return jsonify({'Error': 'No existen datos actualizados'}), 400

    producto = Productos.query.get(idproducto)
    if not producto:
        return jsonify({'Error': 'No existe el prodducto'}), 400

    if 'nombre' in producto_actualizado:
        producto.nombre = producto_actualizado['nombre']
    if 'tipoproducto' in producto_actualizado:
        producto.tipoproducto = producto_actualizado['tipoproducto']
    if 'precio' in producto_actualizado:
        producto.precio = producto_actualizado['precio']
    if 'stock' in producto_actualizado:
        producto.stock = producto_actualizado['stock']

    db.session.commit()
    return jsonify({
        'id': producto.idproducto,
        'nombre': producto.nombre,
        'tipoproducto': producto.tipoproducto,
        'precio': producto.precio,
        'stock': producto.stock,
    }), 200


@app.route('/productos', methods=['POST'])
def crear_producto():
    datos_producto = request.get_json()
    if not datos_producto:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    nuevo_producto = Productos(
        nombre=datos_producto['nombre'],
        tipoproducto=datos_producto['tipoproducto'],
        precio=datos_producto['precio'],
        stock=datos_producto['stock'],
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({
        'nombre': nuevo_producto.nombre,
        'tipoproducto': nuevo_producto.tipoproducto,
        'stock': nuevo_producto.stock,
        'precio': nuevo_producto.precio,

    }), 201


@app.route('/productos/<int:idproducto>', methods=['DELETE'])
def eliminar_producto(idproducto):
    producto = Productos.query.get(idproducto)
    if not producto:
        return jsonify({'Error': 'No existe el producto'}), 400
    else:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'Mensaje': 'Producto eliminaddo correctamente'}), 200


@app.route('/')
def index():
    productos = Productos.query.all()
    usuarios = Usuarios.query.all()
    for usuario in usuarios:
        print(usuario.nombre)
    
    for producto in productos:
        print(producto.nombre)

    return 'Consulta realizada con éxito de usuarios y productos'


@app.route('/usuarios/<int:idusuario>', methods=['GET'])
def obtener_usuario(idusuario):
    usuario = db.session.query(Usuarios).get(idusuario)

    usuario_serializado = {
        'id': usuario.idusuario,
        'nombre': usuario.nombre,
        'contrasenia': usuario.contrasenia,
        'email': usuario.email,
        'monto': usuario.monto,
    }
    return jsonify(usuario_serializado), 200

@app.route('/usuarios/<int:idusuario>', methods=['PUT'])
def actualizar_usuario(idusuario):
    datos_actualizados = request.get_json()
    if not datos_actualizados:
        return jsonify({'Error': 'No existen datos actualizados'}), 400
    

    usuario = db.session.query(Usuarios).get(idusuario)
    if not usuario:
        return jsonify({'Error': 'No existe el usuarios'}), 400

    if 'nombre' in datos_actualizados:
        usuario.nombre = datos_actualizados['nombre']
    if 'contrasenia' in datos_actualizados:
        usuario.contrasenia = datos_actualizados['contrasenia']
    if 'email' in datos_actualizados:
        usuario.email = datos_actualizados['email']
    if 'monto' in datos_actualizados:
        usuario.monto = datos_actualizados['monto']

    db.session.commit()
    return jsonify({
        'id': usuario.idusuario,
        'nombre': usuario.nombre,
        'contrasenia': usuario.contrasenia,
        'email': usuario.email,
        'monto': usuario.monto,
    }), 200



@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos_usuario = request.get_json()
    if not datos_usuario:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    nuevo_usuario = Usuarios(
        nombre=datos_usuario['nombre'],
        contrasenia=datos_usuario['contrasenia'],
        email=datos_usuario['email'],
        monto=datos_usuario['monto'],
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({

        'nombre': nuevo_usuario.nombre,
        'contrasenia': nuevo_usuario.contrasenia,
        'email': nuevo_usuario.email,
        'monto': nuevo_usuario.monto,

    }), 201


@app.route('/usuarios/<int:idusuario>', methods=['DELETE'])
def eliminar_usuario(idusuario):
    usuarios = Usuarios.query.get(idusuario)
    usuario = Usuarios.query.get(idusuario)
    if not usuario:
        return jsonify({'Error': 'No existe el usuario'}), 400
    else:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'Mensaje': 'Usuario eliminaddo correctamente'}), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)

