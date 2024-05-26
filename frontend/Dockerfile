# frontend/Dockerfile
FROM python:3.9.19-alpine3.20

# Instalar pipenv y Flask
RUN pip install pipenv

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el Pipfile y Pipfile.lock al contenedor
COPY Pipfile Pipfile.lock ./

# Especificar la versión de Python que se utilizará con pipenv
RUN pipenv --python 3.9

# Instalar dependencias usando pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copiar el resto del código de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que la aplicación correrá
EXPOSE 5002

# Comando por defecto para correr la aplicación
CMD ["pipenv", "run", "python", "app.py"]
