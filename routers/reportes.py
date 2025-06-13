from fastapi import APIRouter, Response
from utils.pdf_generator import generar_pdf_reporte
from services.firestore_service import db
from google.cloud.firestore_v1.base_query import FieldFilter

router = APIRouter()

@router.get("/reporte/pdf")
async def descargar_reporte():
    datos = []
    becas_ref = db.collection("becas")
    docs = becas_ref.stream()
    for doc in docs:
        datos.append(doc.to_dict())

    pdf_bytes = generar_pdf_reporte(datos)
    return Response(content=pdf_bytes, media_type="application/pdf")
