from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db?charset=utf8mb4')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# class Cabins(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(255))
#     descripcion = db.Column(db.Text)
#     imagen = db.Column(db.Text)

class Cabins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #cabin_id = db.Column(db.Integer, db.ForeignKey('cabins.id'))
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10,2))
    imagen = db.Column(db.Text)

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# @app.route('/cabins')
# def get_all_cabins():
#     cabins = Cabins.query.all()
# 
#     results = []
#     for cabin in cabins:
#         result = {
#             'id': cabin.id,
#             'nombre': cabin.nombre,
#             'descripcion': cabin.descripcion,
#             'imagen': cabin.imagen
#         }
#         results.append(result)
# 
#     return jsonify(results)
# 
# @app.route('/cabins/<int:id>')
# def get_cabin(id):
#     cabin = Cabins.query.get(id)
# 
#     if cabin is None:
#         return jsonify({'error': 'La cabaña no se ha encontrado'}), 404
# 
#     result = {
#         'id': cabin.id,
#         'nombre': cabin.nombre,
#         'descripcion': cabin.descripcion,
#         'imagen': cabin.imagen
#     }
# 
#     return jsonify(result)

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
            # 'cabin_id': cabin.cabin_id,
            'nombre': cabin.nombre,
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
        nameCabin = request.json
        if nameCabin is None:
            return jsonify({"error": "No JSON data found"}), 400
        nombre = nameCabin['nombre']
        cabin = Cabins.query.filter_by(nombre=nombre).first()
        db.session.delete(cabin)
        db.session.commit()
        return jsonify({"message": "Cabaña eliminada con éxito", "Nombre de cabaña": nombre}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_cabin', methods=['PUT'])
def update_cabin():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "No JSON data found"}), 400

        nombre = data['nombre']
        modificarCampo =  data['modificarCampo']
        modificarValor = data['modificarValor']
        cabin = Cabins.query.filter_by(nombre=nombre).first()

        if cabin is None:
            return jsonify({"error": "Cabaña no encontrada"}), 404

        if(modificarCampo == 'nombre'):
            cabin.nombre = modificarValor
            message1 = "Nombre de cabaña actualizado con éxito"
            message2 = "Nuevo nombre de la cabaña"
        elif(modificarCampo == 'descripcion'):
            cabin.descripcion = modificarValor
            message1 = "Descripción de cabaña actualizado con éxito"
            message2 = "Nueva descripción de la cabaña"
        elif(modificarCampo == 'precio'):
            cabin.precio = modificarValor
            message1 = "Precio de cabaña actualizado con éxito"
            message2 = "Nuevo precio de la cabaña"
        elif(modificarCampo == 'imagen'):
            cabin.imagen = modificarValor
            message1 = "Imagen de cabaña actualizado con éxito"
            message2 = "Nueva imagen de la cabaña"
        else:
            return jsonify({"error": "Campo no valido"}), 400

        db.session.commit()
        return jsonify({"message": message1,"Cabaña modificada": nombre ,message2: modificarValor}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
