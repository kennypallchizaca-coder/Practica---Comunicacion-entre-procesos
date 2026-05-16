
from fastapi import FastAPI, HTTPException  # type: ignore[reportMissingImports]
from pydantic import BaseModel  # type: ignore[reportMissingImports]

app = FastAPI()

# Diccionario simple para guardar datos en memoria
db = {}
id_actual = 1

# Esquema simple para recibir datos en POST
class Tarea(BaseModel):
    titulo: str
    descripcion: str

# 1. GET: Listar todas
@app.get("/tareas")
def listar():
    return list(db.values())

# 2. GET: Obtener una por ID o dar error 404
@app.get("/tareas/{id}")
def obtener(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Tarea no existe")
    return db[id]

# 3. POST: Crear nueva tarea (retorna 201)
@app.post("/tareas", status_code=201)
def crear(t: Tarea):
    global id_actual
    db[id_actual] = {
        "id": id_actual, 
        "titulo": t.titulo, 
        "descripcion": t.descripcion, 
        "completada": False
    }
    id_actual += 1
    return db[id_actual - 1]

# 4. PUT: Marcar como completada
@app.put("/tareas/{id}")
def completar(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Tarea no existe")
    db[id]["completada"] = True
    return db[id]

# 5. DELETE: Eliminar
@app.delete("/tareas/{id}")
def eliminar(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Tarea no existe")
    del db[id]
    return {"mensaje": "Eliminada con éxito"}

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="127.0.0.1", port=8000)