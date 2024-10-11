# Usar la imagen de Python Slim como base
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install "fastapi[standard]"
RUN pip3 install pydantic
RUN pip3 install mysql-connector-python

# Copiar el código de la aplicación a /app dentro del contenedor
COPY . .

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8080

# Definir el comando para iniciar la aplicación usando uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
