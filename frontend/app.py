# frontend/app.py
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habitaciones')
def habitaciones():
# Hacer la solicitud GET a la API del backend para obtener los datos
    response = requests.get('http://backend:5001/habitaciones')
    # Si la solicitud es exitosa, obtener los datos en formato JSON
    if response.status_code == 200:
        datos = response.json()
        # Renderizar la plantilla HTML con los datos obtenidos
        return render_template('habitaciones.html', datos=datos)
    else:
        # Si la solicitud falla, mostrar un mensaje de error
        return "Error al obtener los datos del backend"

@app.route('/habitacion/<int:id>')
def habitacion(id):
    response = requests.get(f'http://backend:5001/habitaciones/{id}')
    if response.status_code == 200:
        habitacion = response.json()
        return render_template('habitacion.html', habitacion=habitacion)
    else:
        return "Error al obtener los datos del backend"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
