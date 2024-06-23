from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db?charset=utf8mb4')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cabins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    capacidad = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10,2))
    imagen = db.Column(db.Text)

class Reservas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabin_id = db.Column(db.Integer, db.ForeignKey('cabins.id'))
    nombre = db.Column(db.String(255), nullable=False)
    cantidad_personas = db.Column(db.Integer)
    fecha_ingreso = db.Column(db.Date)
    fecha_salida = db.Column(db.Date)

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response






@app.route('/cabins')
def get_cabins():
    min_precio = request.args.get('min_precio', default=None, type=float)
    max_precio = request.args.get('max_precio', default=None, type=float)

    query = Cabins.query

    if min_precio is not None:
        query = query.filter(Cabins.precio >= min_precio)

    if max_precio is not None:
        query = query.filter(Cabins.precio <= max_precio)

    cabins = query.all()

    results = []
    for cabin in cabins:
        result = {
            'id': cabin.id,
            'nombre': cabin.nombre,
            'capacidad': cabin.capacidad,
            'descripcion': cabin.descripcion,
            'precio': str(cabin.precio),
            'imagen': cabin.imagen
        }
        results.append(result)

    return jsonify(results)

@app.route('/cabins/<int:id>')
def get_room(id):
    cabin = Cabins.query.get(id)

    if cabin is None:
        return jsonify({'error': 'La cabaña no se ha encontrado'}), 404

    result = {
        'id': cabin.id,
        'nombre': cabin.nombre,
        'capacidad': cabin.capacidad,
        'descripcion': cabin.descripcion,
        'precio': str(cabin.precio),
        'imagen': cabin.imagen
    }

    return jsonify(result)

@app.route('/create_cabin', methods=['POST'])
def create_cabin():
    try:
        dataCabin = request.json
        if dataCabin is None:
                return jsonify({"error": "No JSON data found"}), 400
        cabin = Cabins()
        cabin.nombre = dataCabin['nombre']
        cabin.capacidad=dataCabin['capacidad']
        cabin.descripcion = dataCabin['descripcion']
        cabin.precio = dataCabin['precio']
        cabin.imagen = dataCabin['imagen']
        db.session.add(cabin)
        db.session.commit()
        return jsonify({"message": "Cabaña agregada con exito", "data": dataCabin}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/delete_cabin', methods=['DELETE'])
def delete_cabin():
    try:
        idCabin = request.json
        if idCabin is None:
            return jsonify({"error": "No JSON data found"}), 400
        idd = idCabin['id']
        cabin = Cabins.query.get(idd)
        db.session.delete(cabin)
        db.session.commit()
        return jsonify({"message": "Cabaña eliminada con éxito", "ID de cabaña": idd}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_cabin', methods=['PUT'])
def update_cabin():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "No JSON data found"}), 400

        nombre = data['nombre']
        modificarCampos =  data['modificarCampos']
        modificarValores = data['modificarValores']
        cabin = Cabins.query.filter_by(nombre=nombre).first()
        
        if cabin is None:
            return jsonify({"error": "Cabaña no encontrada"}), 404
        for index, campo in enumerate(modificarCampos):
            if(campo == 'nombre'):
                cabin.nombre = modificarValores[index]
            elif(campo == 'capacidad'):
                cabin.capacidad = modificarValores[index]
            elif(campo == 'descripcion'):
                cabin.descripcion = modificarValores[index]
            elif(campo == 'precio'):
                cabin.precio = modificarValores[index]
            elif(campo == 'imagen'):
                cabin.imagen = modificarValores[index]
            else:
                return jsonify({"error": "Campo no valido"}), 400

        db.session.commit()
        return jsonify({"message": "Parámetros actualizados con éxito","Cabaña modificada": nombre, "Parámetros_actualizados": modificarCampos, "Nuevos parámetros": modificarValores}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()
    reserva = Reservas(cabin_id=data['cabin_id'], nombre=data['nombre'], cantidad_personas=data['cantidad_personas'], fecha_ingreso=data['fecha_ingreso'], fecha_salida=data['fecha_salida'])
    db.session.add(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva created'}), 201

@app.route('/reservas/<int:id>', methods=['GET'])
def get_reserva(id):
    reserva = Reservas.query.get(id)
    if reserva is None:
        return jsonify({'error': 'Reserva not found'}), 404
    return jsonify({'id': reserva.id, 'cabin_id': reserva.cabin_id, 'nombre': reserva.nombre, 'cantidad_personas': reserva.cantidad_personas, 'fecha_ingreso': str(reserva.fecha_ingreso), 'fecha_salida': str(reserva.fecha_salida)})

@app.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    data = request.get_json()
    reserva = Reservas.query.get(id)
    if reserva is None:
        return jsonify({'error': 'Reserva not found'}), 404
    if 'cabin_id' in data:
        reserva.cabin_id = data['cabin_id']
    if 'nombre' in data:
        reserva.nombre = data['nombre']
    if 'cantidad_personas' in data:
        reserva.cantidad_personas = data['cantidad_personas']
    if 'fecha_ingreso' in data:
        reserva.fecha_ingreso = data['fecha_ingreso']
    if 'fecha_salida' in data:
        reserva.fecha_salida = data['fecha_salida']
    db.session.commit()
    return jsonify({'message': 'Reserva updated'})

@app.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reservas.query.get(id)
    if reserva is None:
        return jsonify({'error': 'Reserva not found'}), 404
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva deleted'})

@app.route('/filter_cabins', methods=['GET'])
def filter_search():
    fecha_ingreso = request.args.get('fechaIngreso')
    fecha_salida = request.args.get('fechaSalida')
    capacidad = request.args.get('personas')

    if not fecha_ingreso or not fecha_salida or not capacidad:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d').date()
        capacidad = int(capacidad)
    except ValueError:
        return jsonify({'error': 'Invalid parameters'}), 400

    # Obtener habitaciones con la capacidad requerida
    cabins= Cabins.query.filter(Cabins.capacidad >= capacidad).all()

    # Filtrar habitaciones no disponibles en el rango de fechas
    available_cabins = []
    for cabin in cabins:
        reservas = Reservas.query.filter(
            Reservas.cabin_id == cabin.id,
            Reservas.fecha_salida > fecha_ingreso,
            Reservas.fecha_ingreso < fecha_salida
        ).all()
        if not reservas:
            available_cabins.append(cabin)

    # Convertir a diccionario para la respuesta JSON
    resultado = [
        {
            'id': cabin.id,
            'nombre': cabin.nombre,
            'capacidad': cabin.capacidad,
            'descripcion': cabin.descripcion,
            'precio': cabin.precio,
            'imagen': cabin.imagen
        } for cabin in available_cabins
    ]

    return jsonify(resultado), 200  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
