from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from datetime import datetime
from collections import defaultdict
import os

def generar_pdf(datos):
    folder = "reportes"
    os.makedirs(folder, exist_ok=True)
    timestamp = int(datetime.now().timestamp())
    filename = f"reporte_becas_{timestamp}.pdf"
    filepath = os.path.join(folder, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    def header_page():
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")
            logo = ImageReader(logo_path)
            c.drawImage(logo, 40, height - 100, width=60, height=60, mask='auto')
        except Exception as e:
            print("⚠️ Error al cargar logo:", e)

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 50, "Reporte Semanal de Becas")

        c.setFont("Helvetica", 10)
        c.drawRightString(width - 40, height - 70, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    def tabla_encabezado(y):
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Nombre")
        c.drawString(180, y, "No. Control")
        c.drawString(280, y, "Carrera")
        c.drawString(410, y, "Estado")
        c.drawString(470, y, "Hora")
        return y - 20

    agrupado = defaultdict(list)
    for item in datos:
        fecha = item.get("fecha")
        if hasattr(fecha, "to_datetime"):
            fecha_obj = fecha.to_datetime()
        elif hasattr(fecha, "timestamp"):
            fecha_obj = fecha
        else:
            fecha_obj = datetime.strptime(str(fecha), "%Y-%m-%d %H:%M")
        fecha_str = fecha_obj.strftime("%d/%m/%Y")
        hora_str = fecha_obj.strftime("%H:%M")
        item["fecha_str"] = fecha_str
        item["hora_str"] = hora_str
        agrupado[fecha_str].append(item)

    y = height - 120
    header_page()
    total_global = 0

    for fecha, items in sorted(agrupado.items()):
        if y < 100:
            c.showPage()
            y = height - 120
            header_page()

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"📅 {fecha} — Becas: {len(items)}")
        y -= 20
        y = tabla_encabezado(y)

        c.setFont("Helvetica", 9)
        for beca in items:
            if y < 60:
                c.showPage()
                y = height - 120
                header_page()
                y = tabla_encabezado(y)

            c.drawString(50, y, beca.get("nombre", "")[:30])
            c.drawString(180, y, beca.get("numero_control", ""))
            c.drawString(280, y, beca.get("carrera", "")[:25])
            c.drawString(410, y, beca.get("estado", ""))
            c.drawString(470, y, beca.get("hora_str", ""))
            y -= 16

        total_global += len(items)
        y -= 10

    # Conteo total
    if y < 100:
        c.showPage()
        y = height - 120
        header_page()

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, y, f"✅ Total de becas registradas esta semana: {total_global}")
    y -= 40

    # Firma
    c.setFont("Helvetica", 10)
    c.drawString(60, y, "Atentamente,")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y - 16, "Cafetería NutriFOX")

    c.line(60, y - 30, 250, y - 30)  # Línea de firma
    c.drawString(60, y - 45, "Firma responsable")

    c.save()
    return filepath
