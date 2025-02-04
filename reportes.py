from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import io

def generar_reporte_mantenimientos(mantenimientos, desde, hasta):
    c = canvas.Canvas(f"Reporte_Mantenimientos_{desde}_a_{hasta}.pdf", pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Reporte de Mantenimientos del {desde} al {hasta}")
    y -= 30

    c.setFont("Helvetica", 12)
    for m in mantenimientos:
        texto = f"ID: {m[0]} | Maquinaria: {m[1]} | Fecha: {m[2]} | Servicio: {m[3]}"
        c.drawString(50, y, texto)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    # Generar gráfico
    fechas = [m[2] for m in mantenimientos]
    maquinaria = [m[1] for m in mantenimientos]
    plt.figure(figsize=(6, 4))
    plt.bar(fechas, range(len(maquinaria)))
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad de Mantenimientos')
    plt.title('Mantenimientos por Fecha')
    plt.tight_layout()

    # Guardar gráfico en memoria
    imgdata = io.BytesIO()
    plt.savefig(imgdata, format='PNG')
    imgdata.seek(0)
    c.showPage()
    c.drawImage(ImageReader(imgdata), 50, 400, width=500, height=300)
    plt.close()

    c.save()

def generar_reporte_inventario(productos):
    c = canvas.Canvas("Reporte_Inventario.pdf", pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Reporte de Inventario Actual")
    y -= 30

    c.setFont("Helvetica", 12)
    for p in productos:
        texto = f"ID: {p[0]} | Producto: {p[1]} | Stock: {p[3]}"
        c.drawString(50, y, texto)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    # Generar gráfico
    nombres = [p[1] for p in productos]
    stock = [p[3] for p in productos]
    plt.figure(figsize=(6, 4))
    plt.barh(nombres, stock)
    plt.xlabel('Stock')
    plt.ylabel('Producto')
    plt.title('Stock de Productos')
    plt.tight_layout()

    # Guardar gráfico en memoria
    imgdata = io.BytesIO()
    plt.savefig(imgdata, format='PNG')
    imgdata.seek(0)
    c.showPage()
    c.drawImage(ImageReader(imgdata), 50, 400, width=500, height=300)
    plt.close()

    c.save()
