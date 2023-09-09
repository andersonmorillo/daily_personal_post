from fastapi import FastAPI # 1. Importar framework

app = FastAPI() # 2. Crear una instancia de FastAPI

@app.get("/home") # 3. Establecer ruta "/home"
def hola(): # 4. Crear función llamada hola 
    return {"respuesta": "hola mundo"} # 5. Establecer la respuesta