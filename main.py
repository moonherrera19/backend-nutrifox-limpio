# main.py
from fastapi import FastAPI
from routers import becas, usuarios, reportes  # 👈 Asegúrate que "reportes" está aquí

app = FastAPI()

# ✅ Registrar todos los routers
app.include_router(becas.router)
app.include_router(usuarios.router)
app.include_router(reportes.router)  # 👈 Este habilita /reporte/pdf

# (Opcional) Ruta raíz para verificar que el backend funciona
@app.get("/")
def read_root():
    return {"message": "NutriFOX backend activo"}
