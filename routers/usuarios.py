from fastapi import APIRouter, HTTPException
from services.firestore_service import db

router = APIRouter()

@router.get("/email/{email}")
def get_usuario_by_email(email: str):
    docs = db.collection("users").where("email", "==", email).stream()
    for doc in docs:
        return doc.to_dict()
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("/numero_control/{numero}")
def get_usuario_by_control(numero: str):
    docs = db.collection("users").where("numero_control", "==", numero).stream()
    for doc in docs:
        return doc.to_dict()
    raise HTTPException(status_code=404, detail="Usuario no encontrado")