from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_summary_pdf(summary_text: str) -> bytes:
    """
    Génère un rapport PDF à partir d'un texte de résumé.
    Retourne le contenu du PDF sous forme de bytes (compatible Streamlit download).
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 80
    for line in summary_text.split("\n"):
        c.drawString(50, y, line[:110])  # Limite à 110 caractères par ligne
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 80

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
