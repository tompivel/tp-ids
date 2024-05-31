from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
