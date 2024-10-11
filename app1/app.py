from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mysql.connector
from typing import List, Optional

app = FastAPI()

# Configuración de la conexión a MySQL
host_name = "52.23.183.197"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "db_books"

# Esquemas para los modelos
class Libro(BaseModel):
    Título: str
    ID_autor: int
    ISBN: str
    Género: str
    Fecha_publicación: str
    Número_páginas: int
    Editorial: str
    Idioma: str
    Resumen: str
    Disponibilidad: bool

class Autor(BaseModel):
    Nombre: str
    Fecha_nacimiento: str
    Nacionalidad: str
    Biografía: str
    
# Get echo test for load balancer's health check
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}
    
# Obtener todos los libros
@app.get("/libros", response_model=List[Libro])
def get_libros():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Libros")
    libros = cursor.fetchall()
    cursor.close()
    mydb.close()
    
    result = []
    for row in libros:
        result.append({
            'ID_libro': row[0],
            'Título': row[1],
            'ID_autor': row[2],
            'ISBN': row[3],
            'Género': row[4],
            'Fecha_publicación': str(row[5]),
            'Número_páginas': row[6],
            'Editorial': row[7],
            'Idioma': row[8],
            'Resumen': row[9],
            'Disponibilidad': row[10]
        })
    return result

# Obtener un libro por su ID
@app.get("/libros/{id}", response_model=Libro)
def get_libro(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Libros WHERE ID_libro = %s", (id,))
    libro = cursor.fetchone()
    cursor.close()
    mydb.close()
    
    if libro:
        return {
            'ID_libro': libro[0],
            'Título': libro[1],
            'ID_autor': libro[2],
            'ISBN': libro[3],
            'Género': libro[4],
            'Fecha_publicación': str(libro[5]),
            'Número_páginas': libro[6],
            'Editorial': libro[7],
            'Idioma': libro[8],
            'Resumen': libro[9],
            'Disponibilidad': libro[10]
        }
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Crear un nuevo libro
@app.post("/libros", response_model=dict)
def create_libro(item: Libro):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()

    query = """
    INSERT INTO Libros (Título, ID_autor, ISBN, Género, Fecha_publicación, Número_páginas, Editorial, Idioma, Resumen, Disponibilidad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (item.Título, item.ID_autor, item.ISBN, item.Género, item.Fecha_publicación, item.Número_páginas, item.Editorial, item.Idioma, item.Resumen, item.Disponibilidad))
    mydb.commit()
    cursor.close()
    mydb.close()

    return {"message": "Libro creado exitosamente"}

# Actualizar un libro existente
@app.put("/libros/{id}", response_model=dict)
def update_libro(id: int, item: Libro):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()

    query = """
    UPDATE Libros 
    SET Título=%s, ID_autor=%s, ISBN=%s, Género=%s, Fecha_publicación=%s, Número_páginas=%s, Editorial=%s, Idioma=%s, Resumen=%s, Disponibilidad=%s 
    WHERE ID_libro=%s
    """
    cursor.execute(query, (item.Título, item.ID_autor, item.ISBN, item.Género, item.Fecha_publicación, item.Número_páginas, item.Editorial, item.Idioma, item.Resumen, item.Disponibilidad, id))
    mydb.commit()
    cursor.close()
    mydb.close()

    return {"message": "Libro actualizado exitosamente"}

# Eliminar un libro
@app.delete("/libros/{id}", response_model=dict)
def delete_libro(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM Libros WHERE ID_libro=%s", (id,))
    mydb.commit()
    cursor.close()
    mydb.close()

    return {"message": "Libro eliminado exitosamente"}

### CRUD para la tabla "Autor" ###

# Obtener todos los autores
@app.get("/autores", response_model=List[Autor])
def get_autores():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Autor")
    autores = cursor.fetchall()
    cursor.close()
    mydb.close()
    
    result = []
    for row in autores:
        result.append({
            'ID_autor': row[0],
            'Nombre': row[1],
            'Fecha_nacimiento': str(row[2]),
            'Nacionalidad': row[3],
            'Biografía': row[4]
        })
    return result

# Obtener un autor por su ID
@app.get("/autores/{id}", response_model=Autor)
def get_autor(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Autor WHERE ID_autor = %s", (id,))
    autor = cursor.fetchone()
    cursor.close()
    mydb.close()

    if autor:
        return {
            'ID_autor': autor[0],
            'Nombre': autor[1],
            'Fecha_nacimiento': str(autor[2]),
            'Nacionalidad': autor[3],
            'Biografía': autor[4]
        }
    raise HTTPException(status_code=404, detail="Autor no encontrado")

# Crear un nuevo autor
@app.post("/autores", response_model=dict)
def create_autor(item: Autor):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()

    query = """
    INSERT INTO Autor (Nombre, Fecha_nacimiento, Nacionalidad, Biografía)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (item.Nombre, item.Fecha_nacimiento, item.Nacionalidad, item.Biografía))
    mydb.commit()
    cursor.close()
    mydb.close()

    return {"message": "Autor creado exitosamente"}

# Actualizar un autor existente
@app.put("/autores/{id}", response_model=dict)
def update_autor(id: int, item: Autor):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()

    query = """
    UPDATE Autor 
    SET Nombre=%s, Fecha_nacimiento=%s, Nacionalidad=%s, Biografía=%s 
    WHERE ID_autor=%s
    """
    cursor.execute(query, (item.Nombre, item.Fecha_nacimiento, item.Nacionalidad, item.Biografía, id))
    mydb.commit()
    cursor.close()
    mydb.close()

    return {"message": "Autor actualizado exitosamente"}

# Eliminar un autor
@app.delete("/autores/{id}", response_model=dict)
def delete_autor(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM Autor WHERE ID_autor=%s", (id,))
    mydb.commit()
    cursor.close()
    mydb.close()

    return {"message": "Autor eliminado exitosamente"}


