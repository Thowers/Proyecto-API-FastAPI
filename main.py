from fastapi import FastAPI, HTTPException
from typing import Union
from routes.instrumentos_routes import router as instrumentos_router
from routes.musica_routes import router as canciones_router

app = FastAPI(title="API proyecto")
app.include_router(instrumentos_router, prefix="", tags=["Instrumentos"])
app.include_router(canciones_router, prefix="", tags=["Canciones"])

@app.get("/inst/")
def read_root():
    return {"Mensaje": "Bienvenido a la API de instrumentos musicales"}

@app.get("/mus/")
def read_root_musica():
    return {"Mensaje": "Bienvenido a la API de música"}