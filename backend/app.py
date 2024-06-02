from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TablaEjemplo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    edad = db.Column(db.Integer)

class Cabañas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.Text)

class Habitaciones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabaña_id = db.Column(db.Integer, db.ForeignKey('cabañas.id'))
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10,2))
    imagen = db.Column(db.Text)

@app.route('/datos_ejemplo')
def obtener_datos_ejemplo():
    # Consultar todos los registros de la tabla de ejemplo
    datos = TablaEjemplo.query.all()

    # Crear una lista para almacenar los resultados
    resultados = []

    # Iterar sobre los registros y agregarlos a la lista de resultados
    for dato in datos:
        resultado = {
            'id': dato.id,
            'nombre': dato.nombre,
            'edad': dato.edad
        }
        resultados.append(resultado)

    # Devolver los resultados como respuesta JSON
    return jsonify(resultados)

@app.route('/')
def hello_world():
    return '<h2> Welcome to the backend </h2> <a href="/datos_ejemplo"> <button> Ver Prueba </button> </a>'

@app.route('/cabañas')
def get_all_cabins():
    cabañas = Cabañas.query.all()

    results = []
    for cabaña in cabañas:
        result = {
            'id': cabaña.id,
            'nombre': cabaña.nombre,
            'descripcion': cabaña.descripcion,
            'imagen': cabaña.imagen
        }
        results.append(result)

    return jsonify(results)

@app.route('/habitaciones')
def get_all_rooms():
    cabaña_id = request.args.get('cabaña_id', default=None, type=int)
    min_precio = request.args.get('min_precio', default=None, type=float)
    max_precio = request.args.get('max_precio', default=None, type=float)

    query = Habitaciones.query

    if cabaña_id is not None:
        query = query.filter(Habitaciones.cabaña_id == cabaña_id)

    if min_precio is not None:
        query = query.filter(Habitaciones.precio >= min_precio)

    if max_precio is not None:
        query = query.filter(Habitaciones.precio <= max_precio)

    habitaciones = query.all()

    results = []
    for habitacion in habitaciones:
        result = {
            'id': habitacion.id,
            'cabaña_id': habitacion.cabaña_id,
            'nombre': habitacion.nombre,
            'descripcion': habitacion.descripcion,
            'precio': str(habitacion.precio),
            'imagen': habitacion.imagen
        }
        results.append(result)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
