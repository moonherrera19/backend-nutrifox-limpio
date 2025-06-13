from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
from models.schemas import Beca
from services.firestore_service import db
from utils.pdf_generator import generar_pdf
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/becas", tags=["Becas"])

@router.post("/registrar", summary="Registrar beca diaria")
def registrar_beca(beca: Beca):
    becas_ref = db.collection("becas")
    hoy = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # Verificar si ya se registró una beca hoy
    query = becas_ref.where("numero_control", "==", beca.numero_control).where("fecha", ">=", hoy)
    existentes = list(query.stream())
    if existentes:
        raise HTTPException(status_code=400, detail="El alumno ya recibió beca hoy.")

    beca_dict = beca.dict()
    beca_dict["fecha"] = datetime.utcnow()
    becas_ref.add(beca_dict)
    return {"message": "✅ Beca registrada correctamente."}


@router.get("/hoy", summary="Obtener becas cobradas hoy")
def becas_hoy():
    hoy = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    snapshot = db.collection("becas").where("fecha", ">=", hoy).stream()
    return [doc.to_dict() for doc in snapshot]


@router.get("/semana", summary="Obtener becas de los últimos 7 días")
def becas_semana():
    hace_7_dias = datetime.utcnow() - timedelta(days=7)
    snapshot = db.collection("becas").where("fecha", ">=", hace_7_dias).stream()
    return [doc.to_dict() for doc in snapshot]


@router.get("/reporte/pdf", summary="Descargar reporte semanal de becas en PDF")
def descargar_pdf():
    hace_7_dias = datetime.utcnow() - timedelta(days=7)
    snapshot = db.collection("becas").where("fecha", ">=", hace_7_dias).stream()
    datos = [doc.to_dict() for doc in snapshot]

    # Generar y devolver archivo PDF
    ruta_pdf = generar_pdf(datos)
    if not os.path.exists(ruta_pdf):
        raise HTTPException(status_code=404, detail="❌ El archivo PDF no se generó correctamente.")

    return FileResponse(
        ruta_pdf,
        media_type="application/pdf",
        filename=os.path.basename(ruta_pdf)
    )
