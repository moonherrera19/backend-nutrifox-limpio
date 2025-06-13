from utils.pdf_generator import generar_pdf
from datetime import datetime

# Datos simulados como los que vendrían de Firestore
datos = [
    {
        "nombre": "Luis Gómez",
        "numero_control": "2130001",
        "carrera": "Ingeniería en Sistemas",
        "fecha": datetime.utcnow()
    },
    {
        "nombre": "Hilario Bracamontes",
        "numero_control": "20010038",
        "carrera": "Innovación agrícola sustentable",
        "fecha": datetime.utcnow()
    }
]

# Llamar al generador
ruta = generar_pdf(datos)

print(f"✅ PDF generado en: {ruta}")
