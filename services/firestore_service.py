import os
import firebase_admin
from firebase_admin import credentials, firestore

# 🚨 FORZAR la ruta directamente sin .env
cred_path = "firebase_credentials.json"  # <- asegúrate que este archivo está en la raíz

if not os.path.exists(cred_path):
    raise FileNotFoundError(f"❌ No se encontró el archivo de credenciales en: {cred_path}")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
