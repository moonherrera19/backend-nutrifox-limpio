import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 Leer credenciales desde variable de entorno
cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")

if not cred_json:
    raise ValueError("❌ No se encontró la variable de entorno FIREBASE_CREDENTIALS_JSON")

cred_dict = json.loads(cred_json)

# ✅ Inicializar Firebase sólo si no está ya activo
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
