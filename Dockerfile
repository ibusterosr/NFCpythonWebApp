# Usa la imagen oficial de Python como base
FROM python:3.8-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y la carpeta con tu aplicación al contenedor
COPY requirements.txt /app/
COPY . /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8080, que es el puerto en el que se ejecuta Cloud Run
EXPOSE 8080

# Define la variable de entorno para Flask
ENV FLASK_APP=main.py

# Comando para ejecutar tu aplicación cuando el contenedor se inicia
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
