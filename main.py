import os
from fastapi import FastAPI
from routers import usuarios, becas

app = FastAPI(title="NutriFOX Backend")

# Rutas
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(becas.router, prefix="/becas", tags=["Becas"])

@app.get("/")
def read_root():
    return {"message": "NutriFOX Backend activo 🚀"}

# Solo si ejecutas localmente: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

