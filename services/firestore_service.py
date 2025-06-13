import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Leer JSON desde variable de entorno
cred_json_str = os.getenv("FIREBASE_CREDENTIALS_JSON")

if not cred_json_str:
    raise ValueError("❌ No se encontró la variable de entorno FIREBASE_CREDENTIALS_JSON")

# Convertir el string a un diccionario
cred_dict = json.loads(cred_json_str)

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
