from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# URLs de las tres APIs
LIBROS_API_URL = "http://proyecto-cloud-1714451405.us-east-1.elb.amazonaws.com:8080/docs"
USUARIOS_API_URL = "http://proyecto-cloud-1714451405.us-east-1.elb.amazonaws.com:8002/docs"
EDITORIALES_API_URL = "http://proyecto-cloud-1714451405.us-east-1.elb.amazonaws.com:8083/docs"



# Orquestador - Obtener información combinada de un libro, autor y editorial
@app.get("/orquestador/libro_autor_editorial/{id_libro}")
async def get_libro_autor_editorial(id_libro: int):
    async with httpx.AsyncClient() as client:
        try:
            # Obtener los datos del libro desde la API de Libros
            libro_response = await client.get(f"{LIBROS_API_URL}/libros/{id_libro}")
            libro_response.raise_for_status()
            libro_data = libro_response.json()

            # Obtener los datos del autor desde la API de Usuarios
            autor_id = libro_data["ID_autor"]
            autor_response = await client.get(f"{USUARIOS_API_URL}/usuarios/{autor_id}")
            autor_response.raise_for_status()
            autor_data = autor_response.json()

            # Obtener los datos de la editorial desde la API de Editoriales
            editorial_response = await client.get(f"{EDITORIALES_API_URL}/editoriales/{libro_data['Editorial']}")
            editorial_response.raise_for_status()
            editorial_data = editorial_response.json()

            # Combinamos los datos del libro, autor y editorial en una sola respuesta
            resultado = {
                "libro": libro_data,
                "autor": autor_data,
                "editorial": editorial_data
            }
            return JSONResponse(content=resultado)

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en la API: {e}")


# Orquestador - Crear un libro y un autor
@app.post("/orquestador/crear_libro_y_autor")
async def crear_libro_y_autor(libro_data: dict, autor_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            # Crear autor en la API de Usuarios
            autor_response = await client.post(f"{USUARIOS_API_URL}/usuarios", json=autor_data)
            autor_response.raise_for_status()
            autor_result = autor_response.json()

            # Usar el ID del autor recién creado para asignarlo al libro
            libro_data["ID_autor"] = autor_result["ID"]

            # Crear el libro en la API de Libros
            libro_response = await client.post(f"{LIBROS_API_URL}/libros", json=libro_data)
            libro_response.raise_for_status()

            return {"message": "Libro y autor creados exitosamente"}

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en la API: {e}")


# Orquestador - Eliminar un libro y sus datos relacionados (autor y editorial)
@app.delete("/orquestador/eliminar_libro_autor_editorial/{id_libro}")
async def eliminar_libro_autor_editorial(id_libro: int):
    async with httpx.AsyncClient() as client:
        try:
            # Obtener los datos del libro primero
            libro_response = await client.get(f"{LIBROS_API_URL}/libros/{id_libro}")
            libro_response.raise_for_status()
            libro_data = libro_response.json()

            # Eliminar el libro
            await client.delete(f"{LIBROS_API_URL}/libros/{id_libro}")

            # Eliminar el autor asociado
            await client.delete(f"{USUARIOS_API_URL}/usuarios/{libro_data['ID_autor']}")

            # Eliminar la editorial asociada si no hay otros libros relacionados
            editorial_id = libro_data["Editorial"]
            editorial_response = await client.get(f"{EDITORIALES_API_URL}/editoriales/{editorial_id}")
            editorial_response.raise_for_status()
            editorial_data = editorial_response.json()

            if editorial_data["libros_publicados"] == 1:
                await client.delete(f"{EDITORIALES_API_URL}/editoriales/{editorial_id}")

            return {"message": "Libro, autor y editorial eliminados exitosamente"}

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en la API: {e}")

# Ruta base para verificar el estado de la API
@app.get("/")
def base():
    return {"Estado": "Activo"}