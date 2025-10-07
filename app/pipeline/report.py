from weasyprint import HTML
import io

def generate_summary_pdf(summary_text: str) -> bytes:
    """
    Génère un PDF stylé à partir d'un contenu HTML avec WeasyPrint.
    Retourne le PDF en bytes (compatible Streamlit download).
    """
    # Remplace les sauts de ligne avant de construire le HTML
    safe_summary = summary_text.replace("\n", "<br>")

    html_template = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: 'Arial', sans-serif;
            margin: 2cm;
            color: #333;
          }}
          h1 {{
            color: #0066cc;
            border-bottom: 2px solid #0066cc;
            padding-bottom: 5px;
          }}
          p {{
            line-height: 1.5;
          }}
          .footer {{
            position: fixed;
            bottom: 0;
            font-size: 0.8em;
            color: #888;
          }}
        </style>
      </head>
      <body>
        <h1>Rapport DataAudit.io</h1>
        <p>{safe_summary}</p>
        <div class="footer">Généré automatiquement par DataAudit.io</div>
      </body>
    </html>
    """

    # Génération du PDF en mémoire
    pdf_io = io.BytesIO()
    HTML(string=html_template).write_pdf(target=pdf_io)
    pdf_io.seek(0)
    return pdf_io.getvalue()
