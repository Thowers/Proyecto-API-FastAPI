from fastapi import FastAPI
from typing import Union
from routes.instrumentos_routes import router as instrumentos_router

app = FastAPI(title="API proyecto")
app.include_router(instrumentos_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Mensaje": "Bienvenido a la API de instrumentos musicales"}